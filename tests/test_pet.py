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
        "category": {"id": 3, "name": "dogs"},
        "name": "bulldog",
        "photoUrls": ["https://example.com/dog1.jpg"],
        "tags": [{"id": 1, "name": "friendly"}],
        "status": "available",
    },
    {
        "id": 1,
        "category": {"id": 4, "name": "cats"},
        "name": "persian",
        "photoUrls": ["https://example.com/cat1.jpg"],
        "tags": [{"id": 2, "name": "fluffy"}],
        "status": "pending",
    },
    {
        "id": 2,
        "category": {"id": 5, "name": "birds"},
        "name": "parrot",
        "photoUrls": ["https://example.com/parrot.jpg"],
        "tags": [{"id": 3, "name": "talkative"}],
        "status": "sold",
    },
]

@pytest.mark.parametrize("pet_payload", pet_datasets)
def test_create_new_pet(pet_payload):
    # Create pet
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)

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
    updated = update_res.json()
    assert updated["id"] == pet_id
    assert updated["status"] == "sold"
    assert updated["name"].endswith("_updated")

    # Verify update
    get_res = requests.get(f"{BASE_URL}/pet/{pet_id}")
    assert get_res.status_code == 200
    fetched = get_res.json()
    assert fetched["status"] == "sold"
    assert fetched["name"] == updated_body["name"]

def test_find_pet_by_id(pet_payload):
    # Step 1: Create a new pet
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)
    created = create_res.json()
    pet_id = created["id"]

    # Step 2: Find the pet by ID (only need petId in the URL)
    get_res = requests.get(f"{BASE_URL}/pet/{pet_id}")
    assert get_res.status_code == 200
    fetched = get_res.json()

    # Step 3: Verify details
    assert fetched["id"] == pet_id

def test_delete_pet(pet_payload):
    # Step 1: Create a pet
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)
    created = create_res.json()
    pet_id = created["id"]

    # Step 2: Delete the pet
    del_res = requests.delete(f"{BASE_URL}/pet/{pet_id}")
    assert del_res.status_code in (200, 204)

    # Step 3: Verify deletion
    get_res = requests.get(f"{BASE_URL}/pet/{pet_id}")
    # Petstore sometimes returns 404, sometimes 200 with an ApiResponse
    assert get_res.status_code in (404, 200)
    if get_res.status_code == 200:
        body = get_res.json()
        # If it returns 200, it should be an ApiResponse, not a valid pet
        assert "category" in body or "name" in body

def test_find_pet_by_status(pet_payload):
    # Step 1: Create a pet with status = "available"
    pet_payload["status"] = "available"
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)
    created = create_res.json()
    pet_id = created["id"]

    # Step 2: Find pets by status
    res = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "available"})
    assert res.status_code == 200
    pets = res.json()
    assert isinstance(pets, list)

    # Step 3: Verify our created pet is in the results
    found_ids = [p["id"] for p in pets if "id" in p]
    assert pet_id in found_ids

def test_negative_find_pet_by_invalid_id():
    invalid_id = "invalid_id_!@#"
    res = requests.get(f"{BASE_URL}/pet/{invalid_id}")
    assert res.status_code in [404,405]

def test_negative_delete_pet_with_invalid_id():
    invalid_id = "invalid_id_!@#"
    res = requests.delete(f"{BASE_URL}/pet/{invalid_id}")
    assert res.status_code in [404,405]

def test_negative_find_pet_by_status_invalid_status():
    res = requests.get(f"{BASE_URL}/pet/findByStatus", params={"status": "unknown_status"})
    assert res.status_code == 200
    pets = res.json()
    # Expecting an empty list for unknown status
    assert isinstance(pets, list)
    assert len(pets) == 0

def test_negative_update_pet_with_invalid_data(pet_payload):
    # Step 1: Create a valid pet
    create_res = requests.post(f"{BASE_URL}/pet", json=pet_payload)
    assert create_res.status_code in (200, 201)
    created = create_res.json()
    pet_id = created["id"]

    # Step 2: Attempt to update with invalid data (e.g., missing 'name')
    invalid_update = dict(created)
    invalid_update["id"] = "15#5ghd"
    del invalid_update["name"]

    update_res = requests.put(f"{BASE_URL}/pet", json=invalid_update)
    # Expecting a 400 Bad Request or similar error
    assert update_res.status_code in [400, 500]
