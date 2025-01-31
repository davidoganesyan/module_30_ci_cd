from pydantic import BaseModel, ConfigDict


class RecipeIn(BaseModel):
    name: str
    views: int
    cooking_time: int
    ingredients: str
    descr: str


class RecipeOutFirst(BaseModel):
    name: str
    views: int
    cooking_time: int

    model_config = ConfigDict(from_attributes=True)


class RecipeOutSecond(BaseModel):
    name: str
    cooking_time: int
    ingredients: str
    descr: str

    model_config = ConfigDict(from_attributes=True)
