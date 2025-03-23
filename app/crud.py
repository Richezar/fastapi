from models import Advertisement, ORM_CLS, ORM_OBJ
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select

async def add_item(session: AsyncSession, item: ORM_OBJ):
    session.add(item)
    try:
        await session.commit()
    except IntegrityError:
        raise HTTPException(409, 'Item already exists')

async def get_item_by_id(session: AsyncSession, orm_cls: ORM_CLS, item_id: int):
    orm_obj = await session.get(orm_cls, item_id)
    if orm_obj is None:
        raise HTTPException(404, 'item not found')
    return orm_obj

async def delete_item(session: AsyncSession, item: ORM_OBJ):
    item = await session.get(Advertisement, item)
    if not item:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    await session.delete(item)
    await session.commit()
