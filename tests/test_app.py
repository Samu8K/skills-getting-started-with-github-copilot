from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_get_activities_contains_initial_data():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "test_student@example.com"

    # Ensure test email is not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert f"Signed up {email}" in res.json().get("message", "")

    # Verify via GET
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email in data[activity]["participants"]

    # Unregister
    res = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 200
    assert f"Unregistered {email}" in res.json().get("message", "")

    # Verify removal
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert email not in data[activity]["participants"]


def test_unregister_nonexistent_returns_404():
    activity = "Chess Club"
    email = "doesnotexist@example.com"

    # Ensure email not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    res = client.post(f"/activities/{activity}/unregister?email={email}")
    assert res.status_code == 404
    assert res.json().get("detail") == "Participant not found"
