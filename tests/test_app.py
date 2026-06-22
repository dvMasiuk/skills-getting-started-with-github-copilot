import pytest


ACTIVITY_NAME = "Chess Club"
UNKNOWN_ACTIVITY = "Nonexistent Club"
TEST_EMAIL = "test_student@mergington.edu"


def test_root_redirects_to_static_index(client):
    # Arrange
    expected_location = "/static/index.html"

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == expected_location


def test_get_activities_returns_available_activities(client):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert ACTIVITY_NAME in response.json()


def test_signup_for_activity_adds_student_to_participants(client):
    # Arrange
    payload = {"email": TEST_EMAIL}
    original_participants = client.get("/activities").json()[ACTIVITY_NAME]["participants"]
    assert TEST_EMAIL not in original_participants

    # Act
    response = client.post(f"/activities/{ACTIVITY_NAME}/signup", params=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {TEST_EMAIL} for {ACTIVITY_NAME}"
    updated_participants = client.get("/activities").json()[ACTIVITY_NAME]["participants"]
    assert TEST_EMAIL in updated_participants


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    payload = {"email": TEST_EMAIL}

    # Act
    response = client.post(f"/activities/{UNKNOWN_ACTIVITY}/signup", params=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_for_activity_when_student_already_signed_up_returns_400(client):
    # Arrange
    payload = {"email": "michael@mergington.edu"}

    # Act
    response = client.post(f"/activities/{ACTIVITY_NAME}/signup", params=payload)

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_from_activity_removes_student_from_participants(client):
    # Arrange
    payload = {"email": "michael@mergington.edu"}
    original_participants = client.get("/activities").json()[ACTIVITY_NAME]["participants"]
    assert payload["email"] in original_participants

    # Act
    response = client.delete(f"/activities/{ACTIVITY_NAME}/participants", params=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {payload['email']} from {ACTIVITY_NAME}"
    updated_participants = client.get("/activities").json()[ACTIVITY_NAME]["participants"]
    assert payload["email"] not in updated_participants


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    payload = {"email": TEST_EMAIL}

    # Act
    response = client.delete(f"/activities/{UNKNOWN_ACTIVITY}/participants", params=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_student_not_signed_up_returns_404(client):
    # Arrange
    payload = {"email": TEST_EMAIL}

    # Act
    response = client.delete(f"/activities/{ACTIVITY_NAME}/participants", params=payload)

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"
