from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from models import Session
from typing import Annotated

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session

SessionDependancy = Annotated[AsyncSession, Depends(get_session)]