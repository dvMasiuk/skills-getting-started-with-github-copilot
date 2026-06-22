import pytest

from fastapi.testclient import TestClient

from src.app import app, activities


ORIGINAL_ACTIVITIES = {
    activity: {
        "description": data["description"],
        "schedule": data["schedule"],
        "max_participants": data["max_participants"],
        "participants": list(data["participants"]),
    }
    for activity, data in activities.items()
}


@pytest.fixture(scope="function", autouse=True)
def reset_activities():
    activities.clear()
    activities.update({
        activity: {
            "description": data["description"],
            "schedule": data["schedule"],
            "max_participants": data["max_participants"],
            "participants": list(data["participants"]),
        }
        for activity, data in ORIGINAL_ACTIVITIES.items()
    })


@pytest.fixture
def client():
    return TestClient(app)
