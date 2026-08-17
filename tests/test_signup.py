"""Tests for the signup endpoint using AAA (Arrange-Act-Assert) pattern."""


def test_signup_success(client):
    """Test POST /activities/{name}/signup successfully adds participant"""
    # Arrange: Get initial participant count
    response = client.get("/activities")
    initial_count = len(response.json()["Programming Class"]["participants"])
    new_email = "newstudent@mergington.edu"
    
    # Act: Sign up for activity
    response = client.post(
        "/activities/Programming Class/signup",
        params={"email": new_email}
    )
    
    # Assert: Check success response
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    assert new_email in response.json()["message"]
    
    # Verify participant was added
    response = client.get("/activities")
    new_count = len(response.json()["Programming Class"]["participants"])
    assert new_count == initial_count + 1
    assert new_email in response.json()["Programming Class"]["participants"]


def test_signup_duplicate_prevention(client):
    """Test POST signup returns 400 if student already signed up"""
    # Arrange: Get existing participant
    response = client.get("/activities")
    existing_email = response.json()["Chess Club"]["participants"][0]
    
    # Act: Try to sign up duplicate
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email}
    )
    
    # Assert: Check 400 status
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_activity_not_found(client):
    """Test POST signup returns 404 if activity doesn't exist"""
    # Arrange: No setup needed
    
    # Act: Try to sign up for non-existent activity
    response = client.post(
        "/activities/NonExistent/signup",
        params={"email": "test@test.com"}
    )
    
    # Assert: Check 404 status
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_updates_availability(client):
    """Test POST signup correctly updates availability count"""
    # Arrange: Get initial availability
    response = client.get("/activities")
    max_participants = response.json()["Gym Class"]["max_participants"]
    initial_participants = len(response.json()["Gym Class"]["participants"])
    initial_spots_left = max_participants - initial_participants
    
    # Act: Sign up for activity
    response = client.post(
        "/activities/Gym Class/signup",
        params={"email": "newcomer@mergington.edu"}
    )
    
    # Assert: Check spots left decreased
    response = client.get("/activities")
    new_participants = len(response.json()["Gym Class"]["participants"])
    new_spots_left = max_participants - new_participants
    assert new_spots_left == initial_spots_left - 1
    assert new_participants == initial_participants + 1
