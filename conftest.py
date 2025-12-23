sure"""
Configuration and fixtures for pytest.
"""
import pytest
import requests
from faker import Faker

# Initialize Faker for test data generation
faker = Faker()

@pytest.fixture(scope="session")
def base_url():
    """Return the base URL for the API."""
    return "https://jsonplaceholder.typicode.com"

@pytest.fixture(scope="session")
def session():
    """Create a requests session with common headers.
    
    The session is automatically closed after all tests are done.
    """
    session = requests.Session()
    session.headers.update({
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    })
    
    yield session  # Provide the session to tests
    session.close()  # Cleanup after all tests are done

@pytest.fixture
def test_post():
    """Generate test post data."""
    return {
        'title': faker.sentence(),
        'body': faker.paragraph(),
        'userId': 1
    }

@pytest.fixture
def existing_post_id(session, base_url):
    """Get an existing post ID for testing.
    
    This ensures we have a valid ID for update/delete operations.
    """
    response = session.get(f"{base_url}/posts/1")
    return response.json()['id']