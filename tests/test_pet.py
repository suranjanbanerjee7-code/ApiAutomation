import requests
import time
import pytest
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from conftest import BASE_URL

pet_datasets = [
    {
        "id": 0,
        "category": {"id": 1, "name": "dogs"},
        "name": "bulldog",
        "photoUrls": ["https://example.com/dog1.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": "available",
    },
    {
        "id": 0,
        "category": {"id": 2, "name": "cats"},
        "name": "persian",
        "photoUrls": ["https://example.com/cat1.jpg"],
        "tags": [{"id": 2, "name": "fluffy"}],
        "status": "pending",
    },
    {
        "id": 0,
        "category": {"id": 3, "name": "birds"},
        "name": "parrot",
        "photoUrls": ["https://example.com/parrot.jpg"],
        "tags": [{"id": 3, "name": "talkative"}],
        "status": "sold",
    },
]

# @pytest.mark.parametrize("pet_payload", pet_datasets)
# def test_create_new_pet(pet_payload):
#     # Create pet
#     create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
#     assert create_res.status_code in (200, 201)

def test_update_pet_details(pet_payload):
    # First, create a pet to update
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)
    created = create_res.json()
    pet_id = created["id"]

    # Update details
    updated_body = dict(created)
    updated_body["name"] = created["name"] + "_updated"
    updated_body["status"] = "sold"

    update_res = requests.put(f"{BASE_URL}/pet", json=updated_body)
    assert update_res.status_code in (200, 201)
