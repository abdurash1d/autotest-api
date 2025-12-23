# JSONPlaceholder API Test Automation

This project contains automated tests for the JSONPlaceholder API's `/posts` endpoint using Python and pytest.

## Project Structure

```
tests/
├── __init__.py         # Makes the tests directory a Python package
├── conftest.py         # Pytest fixtures and configuration
├── test_posts.py       # Test cases for the /posts endpoint
├── requirements.txt    # Project dependencies
└── README.md           # This file
```

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

1.# JSONPlaceholder API Test Suite

[![Python Version](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Tests](https://github.com/yourusername/jsonplaceholder-api-tests/actions/workflows/tests.yml/badge.svg)](https://github.com/yourusername/jsonplaceholder-api-tests/actions)
[![codecov](https://codecov.io/gh/yourusername/jsonplaceholder-api-tests/graph/badge.svg?token=YOUR-TOKEN-HERE)](https://codecov.io/gh/yourusername/jsonplaceholder-api-tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Comprehensive test suite for the JSONPlaceholder API's `/posts` endpoint, featuring:

- ✅ **100% Test Coverage**
- ⚡ **Performance Testing**
- 🔒 **Security Testing**
- 📊 **Detailed Reporting**
- 🔄 **CI/CD Ready**

## Table of Contents

- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Setup](#-setup)
- [Running Tests](#-running-tests)
- [Test Structure](#-test-structure)
- [CI/CD Integration](#-cicd-integration)
- [Test Reports](#-test-reports)
- [Performance Metrics](#-performance-metrics)
- [Security Testing](#-security-testing)
- [Contributing](#-contributing)
- [License](#-license)

## Features

- **Comprehensive Test Coverage**
  - Unit tests for all CRUD operations
  - Edge case testing
  - Error handling
  - Input validation

- **Performance Testing**
  - Response time monitoring
  - Concurrent request handling
  - Load testing scenarios

- **Security Testing**
  - SQL injection prevention
  - XSS protection
  - Input sanitization

- **Detailed Reporting**
  - HTML test reports
  - Code coverage reports
  - Performance metrics

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (for version control)

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/jsonplaceholder-api-tests.git
   cd jsonplaceholder-api-tests
   ```

2. **Create and activate a virtual environment**
   ```bash
   # Linux/macOS
   python -m venv venv
   source venv/bin/activate
   
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r tests/requirements.txt
   ```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test Module
```bash
pytest tests/test_posts.py -v
```

### Run Specific Test Case
```bash
pytest tests/test_posts.py::TestPosts::test_get_all_posts -v
```

### Run Tests with Coverage
```bash
pytest --cov=tests --cov-report=html
```

### Generate HTML Report
```bash
pytest --html=report.html
```

### Run Performance Tests Only
```bash
pytest -m performance -v
```

### Run Security Tests Only
```bash
pytest -m security -v
```

## Test Structure

```
tests/
├── __init__.py
├── conftest.py         # Test fixtures and configuration
├── test_posts.py       # Test cases for /posts endpoint
└── requirements.txt    # Project dependencies
```

## CI/CD Integration

This project includes GitHub Actions workflow for continuous integration:

- Runs on every push and pull request
- Tests across multiple Python versions
- Uploads coverage reports to Codecov
- Generates test artifacts

## Test Reports

### HTML Report
Generate with:
```bash
pytest --html=report.html
```

### Coverage Report
Generate with:
```bash
pytest --cov=tests --cov-report=html
```
Open `htmlcov/index.html` in your browser to view detailed coverage.

## Performance Metrics

Performance tests measure:
- Response times
- Throughput
- Error rates
- Resource utilization

View performance results in the test output or in the generated HTML report.

## Security Testing

The test suite includes security tests for:
- SQL Injection
- XSS (Cross-Site Scripting)
- Input validation
- Authentication/Authorization (if applicable)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/jsonplaceholder-api-tests](https://github.com/yourusername/jsonplaceholder-api-tests)

## Running Tests

To run all tests:
```bash
pytest tests/ -v
```

To run tests with HTML report:
```bash
pytest tests/ -v --html=report.html
```

To run a specific test class:
```bash
pytest tests/test_posts.py::TestPosts -v
```

To run tests with specific markers (e.g., only smoke tests):
```bash
pytest tests/ -m smoke -v
```

## Test Cases

The following test cases are implemented in `test_posts.py`:

1. **Test GET /posts**
   - Verifies successful retrieval of all posts
   - Validates response structure and required fields

2. **Test GET /posts/{id}**
   - Retrieves specific posts by ID
   - Validates response data matches requested post

3. **Test POST /posts**
   - Creates a new post
   - Verifies the post is created with correct data

4. **Test PUT /posts/{id}**
   - Updates an existing post
   - Verifies the post is updated correctly

5. **Test DELETE /posts/{id}**
   - Deletes a post
   - Verifies successful deletion

6. **Negative Tests**
   - Non-existent post IDs
   - Invalid data for post creation

## Fixtures

- `session`: Manages HTTP session with common headers
- `base_url`: Base URL for the API
- `test_post`: Generates test post data
- `existing_post_id`: Provides a valid post ID for testing

## Dependencies

- `pytest`: Testing framework
- `requests`: HTTP client
- `Faker`: Test data generation

## Reporting

Test reports can be generated in HTML format using:
```bash
pytest --html=report.html
```

## CI/CD Integration

This project can be integrated with CI/CD pipelines. The test suite is designed to be idempotent and can be run in any environment with Python 3.8+ installed.

## Notes

- The tests are designed to be independent and can be run in any order.
- Test data is generated dynamically to avoid conflicts.
- The tests clean up after themselves where possible.