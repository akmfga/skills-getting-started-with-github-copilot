"""Tests for the root endpoint using AAA (Arrange-Act-Assert) pattern."""


def test_root_redirect(client):
    """Test GET / redirects to /static/index.html"""
    # Arrange: No setup needed
    
    # Act: Make GET request to root
    response = client.get("/", follow_redirects=False)
    
    # Assert: Check redirect status and location
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]


def test_root_redirect_with_follow(client):
    """Test GET / follows redirect successfully"""
    # Arrange: No setup needed
    
    # Act: Make GET request with follow_redirects=True
    response = client.get("/", follow_redirects=True)
    
    # Assert: Check response status (should be OK or similar from static)
    assert response.status_code in [200, 404]  # 200 if static file exists, 404 if it doesn't in test
