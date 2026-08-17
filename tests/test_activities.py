"""Tests for the activities endpoint using AAA (Arrange-Act-Assert) pattern."""


def test_get_activities_success(client):
    """Test GET /activities returns all activities"""
    # Arrange: No setup needed (fixture provides initial state)
    
    # Act: Make GET request to /activities
    response = client.get("/activities")
    
    # Assert: Check status and response structure
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_has_correct_fields(client):
    """Test GET /activities returns activities with correct fields"""
    # Arrange: No setup needed
    
    # Act: Get activities
    response = client.get("/activities")
    data = response.json()
    
    # Assert: Check that each activity has required fields
    activity = data["Chess Club"]
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    assert isinstance(activity["participants"], list)


def test_delete_participant_success(client):
    """Test DELETE /activities/{name}/participants/{email} removes participant"""
    # Arrange: Get initial participant count
    response = client.get("/activities")
    initial_participants = response.json()["Chess Club"]["participants"]
    initial_count = len(initial_participants)
    email_to_remove = initial_participants[0]
    
    # Act: Delete participant
    response = client.delete(f"/activities/Chess Club/participants/{email_to_remove}")
    
    # Assert: Check success response
    assert response.status_code == 200
    assert "Removed" in response.json()["message"]
    
    # Verify participant was removed
    response = client.get("/activities")
    new_participants = response.json()["Chess Club"]["participants"]
    assert len(new_participants) == initial_count - 1
    assert email_to_remove not in new_participants


def test_delete_participant_activity_not_found(client):
    """Test DELETE returns 404 when activity doesn't exist"""
    # Arrange: No setup needed
    
    # Act: Try to delete from non-existent activity
    response = client.delete("/activities/NonExistent/participants/test@test.com")
    
    # Assert: Check 404 status
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_delete_participant_not_found(client):
    """Test DELETE returns 404 when participant doesn't exist"""
    # Arrange: No setup needed
    
    # Act: Try to delete non-existent participant
    response = client.delete("/activities/Chess Club/participants/nonexistent@test.com")
    
    # Assert: Check 404 status
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
