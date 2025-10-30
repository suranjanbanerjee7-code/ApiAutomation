import random
import string
import pytest

BASE_URL = "https://petstore.swagger.io/v2"

def rnd_name(prefix="pet"):
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return f"{prefix}-{suffix}"

@pytest.fixture
def pet_payload():
    return {
        "id": 0,
        "category": {"id": 0, "name": "animals"},
        "name": rnd_name(),
        # "photoUrls": ["C:\Users\POJIT\Pictures\Screenshots\pet1.jpg"],
        "photoUrls": ["string"],
        "tags": [{"id": 0, "name": "tag1"}],
        "status": "available",
    }

@pytest.fixture
def order_payload():
    return {
        "id": 0,
        "petId": 0,
        "quantity": 1,
        "shipDate": "2025-01-01T00:00:00.000Z",
        "status": "placed",
        "complete": True
    }