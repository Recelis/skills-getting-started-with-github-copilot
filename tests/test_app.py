from src.app import activities

NEW_EMAIL = "newstudent@mergington.edu"


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client):
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert {"description", "schedule", "max_participants", "participants"} <= data["Chess Club"].keys()


def test_signup_success(client):
    response = client.post("/activities/Chess Club/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 200
    assert NEW_EMAIL in activities["Chess Club"]["participants"]


def test_signup_unknown_activity(client):
    response = client.post("/activities/Nope/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 404


def test_signup_duplicate(client):
    existing = activities["Chess Club"]["participants"][0]
    response = client.post("/activities/Chess Club/signup", params={"email": existing})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_activity_full(client):
    activity = activities["Chess Club"]
    activity["max_participants"] = len(activity["participants"])
    response = client.post("/activities/Chess Club/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_unregister_success(client):
    existing = activities["Chess Club"]["participants"][0]
    response = client.delete("/activities/Chess Club/signup", params={"email": existing})
    assert response.status_code == 200
    assert existing not in activities["Chess Club"]["participants"]


def test_unregister_unknown_activity(client):
    response = client.delete("/activities/Nope/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 404


def test_unregister_not_signed_up(client):
    response = client.delete("/activities/Chess Club/signup", params={"email": NEW_EMAIL})
    assert response.status_code == 404
