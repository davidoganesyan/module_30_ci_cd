import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker  # type: ignore
from sqlalchemy.ext.asyncio import create_async_engine

from database import Base, get_db
from models import Recipe

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine(TEST_DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine):
    async with async_sessionmaker(engine)() as session:
        yield session


@pytest.fixture
async def app(engine):
    app = FastAPI()

    async def override_get_db():
        async with async_sessionmaker(engine)() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    from main import app as main_app

    app.include_router(main_app.router)

    return app


@pytest.fixture
async def client(app):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup(session):
    yield
    await session.execute(Recipe.__table__.delete())
    await session.commit()
