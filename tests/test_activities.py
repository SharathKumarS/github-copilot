def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange
    # (activities are already set up by the reset_activities fixture)
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert len(data) == 2


def test_signup_new_student(client):
    """Test signing up a new student for an activity"""
    # Arrange
    new_email = "newstudent@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    
    # Verify participant was added
    activities_data = client.get("/activities").json()
    assert new_email in activities_data[activity_name]["participants"]


def test_signup_duplicate_student(client):
    """Test that duplicate signups are rejected"""
    # Arrange
    existing_email = "michael@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity(client):
    """Test signing up for an activity that doesn't exist"""
    # Arrange
    email = "student@mergington.edu"
    nonexistent_activity = "Nonexistent Activity"
    
    # Act
    response = client.post(
        f"/activities/{nonexistent_activity}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_student(client):
    """Test unregistering a student from an activity"""
    # Arrange
    email_to_remove = "michael@mergington.edu"
    activity_name = "Chess Club"
    initial_count = len(client.get("/activities").json()[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={email_to_remove}"
    )
    
    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    
    # Verify participant was removed
    final_activities = client.get("/activities").json()
    assert email_to_remove not in final_activities[activity_name]["participants"]
    assert len(final_activities[activity_name]["participants"]) == initial_count - 1


def test_unregister_nonexistent_student(client):
    """Test unregistering a student not registered for activity"""
    # Arrange
    unregistered_email = "notregistered@mergington.edu"
    activity_name = "Chess Club"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister?email={unregistered_email}"
    )
    
    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_from_nonexistent_activity(client):
    """Test unregistering from an activity that doesn't exist"""
    # Arrange
    email = "student@mergington.edu"
    nonexistent_activity = "Nonexistent Activity"
    
    # Act
    response = client.delete(
        f"/activities/{nonexistent_activity}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
