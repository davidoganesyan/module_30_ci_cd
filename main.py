from contextlib import asynccontextmanager
from typing import List, Sequence

from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import models
import schemas
from database import Base, engine, get_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/recipe", response_model=List[schemas.RecipeOutFirst])
async def get_all_recipe(
    db: AsyncSession = Depends(get_db),  # noqa: B008
) -> Sequence[models.Recipe]:
    res = await db.execute(
        select(models.Recipe).order_by(
            models.Recipe.views.desc(), models.Recipe.cooking_time
        )
    )
    return res.scalars().all()


@app.get("/recipe/{idx}", response_model=schemas.RecipeOutSecond)
async def get_recipe_by_id(idx: int, db: AsyncSession = Depends(get_db)):  # noqa: B008
    res = await db.execute(select(models.Recipe).where(models.Recipe.id == idx))
    recipe = res.scalars().one()
    recipe.views += 1
    await db.commit()
    await db.refresh(recipe)
    return recipe


@app.post("/recipe/", response_model=schemas.RecipeIn)
async def add_new_recipe(
    recipe: schemas.RecipeIn, db: AsyncSession = Depends(get_db)  # noqa: B008
) -> models.Recipe:
    new_recipe = models.Recipe(
        name=recipe.name,
        descr=recipe.descr,
        views=recipe.views,
        cooking_time=recipe.cooking_time,
        ingredients=recipe.ingredients,
    )
    db.add(new_recipe)
    await db.commit()
    await db.refresh(new_recipe)
    return new_recipe
