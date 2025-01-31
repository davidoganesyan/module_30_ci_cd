import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_connection(client: AsyncClient):
    response = await client.get("recipe")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_recipe_add(client: AsyncClient):
    response = await client.post(
        "/recipe/",
        json={
            "name": "Test recipe",
            "views": 1,
            "cooking_time": 2,
            "ingredients": "teest",
            "descr": "qwe",
        },
    )
    assert response.status_code == 200

    response = await client.get(f"/recipe/{1}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test recipe"
