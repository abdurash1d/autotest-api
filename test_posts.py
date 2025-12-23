"""
Tests for the /posts endpoint of JSONPlaceholder API.
"""
import json
import time
import pytest
import statistics
from datetime import datetime, timezone
from faker import Faker

# Initialize Faker for generating test data
faker = Faker()

class TestPosts:
    """Test cases for the /posts endpoint."""

    def test_get_all_posts(self, session, base_url):
        """Test GET /posts returns a list of posts with correct structure."""
        start_time = time.time()
        response = session.get(f"{base_url}/posts")
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Response time assertion (adjust threshold as needed)
        assert response_time < 1000, f"Response time {response_time:.2f}ms exceeds 1000ms threshold"
        
        assert response.status_code == 200
        posts = response.json()
        assert isinstance(posts, list)
        
        # Verify each post has required fields
        for post in posts:
            assert 'id' in post
            assert isinstance(post['id'], int)
            assert 'title' in post
            assert isinstance(post['title'], str)
            assert 'body' in post
            assert isinstance(post['body'], str)
            assert 'userId' in post
            assert isinstance(post['userId'], int)
            
            # Additional data quality checks
            assert len(post['title']) > 0, "Post title should not be empty"
            assert len(post['body']) > 0, "Post body should not be empty"
            assert post['userId'] > 0, "User ID should be a positive integer"

    @pytest.mark.parametrize("post_id", [1, 5, 10], ids=["first", "fifth", "tenth"])
    def test_get_single_post(self, session, base_url, post_id):
        """Test GET /posts/{id} returns the correct post."""
        # Test cache headers
        response = session.head(f"{base_url}/posts/{post_id}")
        assert 'etag' in response.headers or 'last-modified' in response.headers, \
            "Response should include caching headers"
            
        # Test with If-None-Match header if ETag is present
        if 'etag' in response.headers:
            etag = response.headers['etag']
            response = session.get(
                f"{base_url}/posts/{post_id}",
                headers={'If-None-Match': etag}
            )
            assert response.status_code == 304, "Should return 304 Not Modified for matching ETag"
        
        # Get the actual post
        response = session.get(f"{base_url}/posts/{post_id}")
        
        # Verify response time
        assert response.elapsed.total_seconds() < 1, "Response time should be under 1 second"
        
        assert response.status_code == 200
        post = response.json()
        
        # Verify response headers
        assert 'content-type' in response.headers
        assert 'application/json' in response.headers['content-type']
        
        # Verify post structure
        assert post['id'] == post_id
        required_fields = ['id', 'title', 'body', 'userId']
        assert all(key in post for key in required_fields), \
            f"Missing required fields in response: {required_fields}"
            
        # Type checking
        assert isinstance(post['id'], int)
        assert isinstance(post['title'], str)
        assert isinstance(post['body'], str)
        assert isinstance(post['userId'], int)
        
        # Data validation
        assert len(post['title']) > 0, "Title should not be empty"
        assert len(post['body']) > 0, "Body should not be empty"
        assert post['userId'] > 0, "User ID should be positive"

    def test_create_post(self, session, base_url, test_post):
        """Test POST /posts creates a new post with valid data."""
        # Test with valid data
        start_time = time.time()
        response = session.post(
            f"{base_url}/posts",
            data=json.dumps(test_post),
            headers={'Content-Type': 'application/json'}
        )
        response_time = (time.time() - start_time) * 1000  # ms
        
        # Performance check
        assert response_time < 2000, f"Create post took {response_time:.2f}ms (expected < 2000ms)"
        
        # Status and content type check
        assert response.status_code == 201, f"Expected 201, got {response.status_code}"
        assert 'content-type' in response.headers
        assert 'application/json' in response.headers['content-type']
        
        created_post = response.json()
        
        # Verify the created post matches the sent data
        assert created_post['title'] == test_post['title']
        assert created_post['body'] == test_post['body']
        assert created_post['userId'] == test_post['userId']
        assert 'id' in created_post
        
        # Verify the post can be retrieved
        response = session.get(f"{base_url}/posts/{created_post['id']}")
        assert response.status_code == 200
        
        # Test with different content types
        for content_type in [
            'application/json',
            'application/json; charset=utf-8',
            'application/json;charset=UTF-8'
        ]:
            response = session.post(
                f"{base_url}/posts",
                data=json.dumps(test_post),
                headers={'Content-Type': content_type}
            )
            assert response.status_code == 201, f"Failed with content-type: {content_type}"

    def test_update_post(self, session, base_url, existing_post_id):
        """Test PUT /posts/{id} updates an existing post."""
        # First get the original post
        get_response = session.get(f"{base_url}/posts/{existing_post_id}")
        original_post = get_response.json()
        
        # Prepare test data with different update scenarios
        test_cases = [
            {
                'name': 'update_all_fields',
                'data': {
                    'title': f'Updated Title {datetime.now(timezone.utc).isoformat()}',
                    'body': f'Updated body content {faker.paragraph()}',
                    'userId': 1
                }
            },
            {
                'name': 'partial_update',
                'data': {
                    'title': f'Partial Update {datetime.now(timezone.utc).isoformat()}',
                    # Omit body and userId to test partial updates
                }
            },
            {
                'name': 'minimal_update',
                'data': {
                    'title': f'Minimal Update {datetime.now(timezone.utc).isoformat()}'
                }
            }
        ]
        
        for test_case in test_cases:
            with self.subTest(test_case['name']):
                # Merge with original data to ensure we have all required fields
                update_data = {**original_post, **test_case['data']}
                
                # Time the update operation
                start_time = time.time()
                response = session.put(
                    f"{base_url}/posts/{existing_post_id}",
                    data=json.dumps(update_data),
                    headers={'Content-Type': 'application/json'}
                )
                response_time = (time.time() - start_time) * 1000  # ms
                
                # Performance check
                assert response_time < 2000, \
                    f"Update post took {response_time:.2f}ms (expected < 2000ms)"
                
                # Verify response
                assert response.status_code == 200, \
                    f"Expected 200, got {response.status_code} for {test_case['name']}"
                
                updated_post = response.json()
                
                # Verify the post was updated correctly
                assert updated_post['id'] == existing_post_id
                for key, value in test_case['data'].items():
                    assert updated_post[key] == value, \
                        f"Field '{key}' not updated correctly in {test_case['name']}"
                
                # Verify the update is persistent
                get_response = session.get(f"{base_url}/posts/{existing_post_id}")
                persisted_post = get_response.json()
                for key, value in test_case['data'].items():
                    assert persisted_post[key] == value, \
                        f"Update not persistent for field '{key}' in {test_case['name']}"

    def test_delete_post(self, session, base_url, existing_post_id):
        """Test DELETE /posts/{id} removes the post."""
        # First verify the post exists
        response = session.get(f"{base_url}/posts/{existing_post_id}")
        assert response.status_code == 200, "Post should exist before deletion"
        
        # Time the delete operation
        start_time = time.time()
        response = session.delete(f"{base_url}/posts/{existing_post_id}")
        response_time = (time.time() - start_time) * 1000  # ms
        
        # Performance check
        assert response_time < 2000, f"Delete operation took {response_time:.2f}ms (expected < 2000ms)"
        
        # Verify response
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        assert response.json() == {}
        
        # Verify the post is actually deleted
        response = session.get(f"{base_url}/posts/{existing_post_id}")
        assert response.status_code == 404, "Post should be deleted"
        
        # Test idempotency - deleting again should still return 200
        response = session.delete(f"{base_url}/posts/{existing_post_id}")
        assert response.status_code in [200, 404], \
            "Subsequent deletes should be idempotent (200 or 404)"

    @pytest.mark.parametrize("invalid_id, expected_status", [
        (0, 404),  # Zero ID
        (-1, 404),  # Negative ID
        (999999, 404),  # Non-existent ID
        ('invalid', 404),  # String ID
        ('1.5', 404),  # Float string ID
        ('1a', 404),  # Alphanumeric
        (' ', 404),  # Whitespace
        ('', 404),  # Empty string
        ('null', 404),  # String 'null'
        ('undefined', 404),  # String 'undefined'
        ('<script>alert(1)</script>', 404),  # XSS attempt
        ('1; DROP TABLE posts', 404),  # SQL injection attempt
        ('1' * 1000, 404),  # Very long ID
        (None, 404),  # None value
    ], ids=[
        'zero', 'negative', 'non_existent', 'string', 'float_string',
        'alphanumeric', 'whitespace', 'empty', 'null_string', 'undefined_string',
        'xss', 'sql_injection', 'long_id', 'none'
    ])
    def test_get_nonexistent_post(self, session, base_url, invalid_id, expected_status):
        """Test GET /posts/{id} with various invalid IDs."""
        url = f"{base_url}/posts/{invalid_id}" if invalid_id is not None else f"{base_url}/posts/"
        
        # Test with different HTTP methods that should be handled
        for method in [session.get, session.head, session.put, session.delete]:
            response = method(url)
            assert response.status_code in [expected_status, 405], \
                f"Unexpected status code {response.status_code} for {method.__name__.upper()} with ID: {invalid_id}"

    @pytest.mark.parametrize("test_data, expected_status, description", [
        # Valid data variations
        ({'title': 'Valid Title', 'body': 'Valid body', 'userId': 1}, 201, 'valid_complete'),
        ({'title': 'X' * 1000, 'body': 'X' * 5000, 'userId': 1}, 201, 'long_fields'),
        ({'title': 'Title with unicode: 😊', 'body': 'Body with unicode: ñáéíóú', 'userId': 1}, 201, 'unicode_chars'),
        ({'title': '  Trim me  ', 'body': '  Trim me too  ', 'userId': 1}, 201, 'whitespace_trimming'),
        
        # Edge cases for title
        ({'title': 'a', 'body': 'Valid body', 'userId': 1}, 201, 'min_length_title'),
        ({'title': 'X' * 255, 'body': 'Valid body', 'userId': 1}, 201, 'max_length_title'),
        
        # Edge cases for body
        ({'title': 'Valid title', 'body': 'a', 'userId': 1}, 201, 'min_length_body'),
        
        # Edge cases for userId
        ({'title': 'Valid title', 'body': 'Valid body', 'userId': 1}, 201, 'min_user_id'),
        ({'title': 'Valid title', 'body': 'Valid body', 'userId': 2**31-1}, 201, 'max_user_id'),
        
        # Invalid data cases (JSONPlaceholder accepts these but we can still test the behavior)
        ({'title': '', 'body': 'Empty title', 'userId': 1}, 201, 'empty_title'),
        ({'title': '   ', 'body': 'Whitespace title', 'userId': 1}, 201, 'whitespace_title'),
        ({'title': 'No body', 'userId': 1}, 201, 'missing_body'),
        ({'body': 'No title', 'userId': 1}, 201, 'missing_title'),
        ({'title': 'No user', 'body': 'No user ID'}, 201, 'missing_user_id'),
        ({'title': None, 'body': 'None title', 'userId': 1}, 201, 'null_title'),
        ({'title': 'None body', 'body': None, 'userId': 1}, 201, 'null_body'),
        ({'title': 'None user', 'body': 'None user ID', 'userId': None}, 201, 'null_user_id'),
        ({'title': 123, 'body': 456, 'userId': '1'}, 201, 'wrong_types'),
        ({'title': {'nested': 'object'}, 'body': ['array'], 'userId': 1}, 201, 'complex_objects'),
        
        # Malformed requests
        ('not a json', 400, 'invalid_json'),
        (None, 400, 'null_payload'),
    ], ids=lambda x: x[2] if isinstance(x, tuple) else str(x))
    def test_create_post_edge_cases(self, session, base_url, test_data, expected_status, description):
        """Test POST /posts with various edge cases and invalid data."""
        headers = {'Content-Type': 'application/json'}
        
        # Skip actual request for malformed JSON test cases
        if description in ['invalid_json', 'null_payload']:
            if description == 'invalid_json':
                data = test_data  # Already a string
            else:  # null_payload
                data = None
        else:
            data = json.dumps(test_data)
        
        # Time the request
        start_time = time.time()
        response = session.post(
            f"{base_url}/posts",
            data=data,
            headers=headers
        )
        response_time = (time.time() - start_time) * 1000  # ms
        
        # Log the test case for debugging
        print(f"\nTest case: {description}")
        print(f"Status: {response.status_code} (expected: {expected_status})")
        print(f"Response time: {response_time:.2f}ms")
        
        # Check response status
        assert response.status_code == expected_status, \
            f"Expected status {expected_status} for {description}, got {response.status_code}"
        
        # For successful creation, verify the response structure
        if response.status_code == 201:
            response_data = response.json()
            assert 'id' in response_data, "Response should contain an 'id' field"
            
            # Check that the response includes all fields from the request
            if isinstance(test_data, dict):
                for key, value in test_data.items():
                    if value is not None:  # Skip None values as they might be omitted
                        if isinstance(value, str):
                            # Check if we expect whitespace trimming
                            if key in ['title', 'body'] and description == 'whitespace_trimming':
                                assert response_data[key] == value.strip(), \
                                    f"{key} should be trimmed"
                            else:
                                assert response_data[key] == value, \
                                    f"{key} does not match in response"
                        else:
                            assert response_data[key] == value, \
                                f"{key} does not match in response"
            
            # Verify default values for missing fields
            if description in ['missing_title', 'missing_body', 'missing_user_id', 
                             'null_title', 'null_body', 'null_user_id']:
                if 'title' not in test_data or test_data['title'] is None:
                    assert 'title' in response_data, "Title should be present in response"
                    assert response_data['title'] == '', "Title should be empty string if not provided"
                if 'body' not in test_data or test_data['body'] is None:
                    assert 'body' in response_data, "Body should be present in response"
                    assert response_data['body'] == '', "Body should be empty string if not provided"
                if 'userId' not in test_data or test_data['userId'] is None:
                    assert 'userId' in response_data, "userId should be present in response"
                    assert response_data['userId'] == 1, "userId should default to 1 if not provided"
        
        # Performance check (only for successful requests)
        if response.status_code == 201:
            assert response_time < 2000, \
                f"Request took {response_time:.2f}ms (expected < 2000ms) for {description}"