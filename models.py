from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column  # type: ignore

from database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    descr: Mapped[str | None] = mapped_column(String)
    views: Mapped[int] = mapped_column(Integer, default=0)
    cooking_time: Mapped[int] = mapped_column(Integer, nullable=False)
    ingredients: Mapped[str] = mapped_column(String, nullable=False)
