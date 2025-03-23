from fastapi import FastAPI, HTTPException, Query
from schema import (CreateAdvertisementRequest,
                    UpdateAdvertisementRequest,
                    CreateAdvertisementResponse,
                    UpdateAdvertisementResponse,
                    DeleteAdvertisementResponse,
                    GetAdvertisementResponse,
                    )
from lifespan import lifespan
from dependancy import SessionDependancy
import crud
import models
from sqlalchemy.future import select

app = FastAPI(
    title='Advertisement',
    lifespan=lifespan
)


@app.post("/advertisement", tags=['Advertisement'], response_model=CreateAdvertisementResponse)
async def create_advertisement(ad: CreateAdvertisementRequest, session: SessionDependancy):
    ad_dict = ad.model_dump(exclude_unset=True)
    ad_orm_obj = models.Advertisement(**ad_dict)
    await crud.add_item(session, ad_orm_obj)
    return ad_orm_obj.id_dict

@app.patch("/advertisement/{ad_id}", tags=['Advertisement'])
async def update_advertisement(ad_id: int, ad_data: UpdateAdvertisementRequest, session: SessionDependancy):
    ad = await session.get(models.Advertisement, ad_id)
    if not ad:
        raise HTTPException(status_code=404, detail="Advertisement not found")
    for field, value in ad_data.dict(exclude_unset=True).items():
        setattr(ad, field, value)
    session.add(ad)
    await session.commit()
    return {"status": "success", "advertisement": ad.dict}

@app.get("/advertisement/{ad_id}", tags=['Advertisement'], response_model=GetAdvertisementResponse)
async def get_advertisement(ad_id: int, session: SessionDependancy):
    ad_orm_obj = await crud.get_item_by_id(session, models.Advertisement, ad_id)
    return ad_orm_obj.dict

@app.get("/advertisement", tags=['Advertisement'], response_model=list[GetAdvertisementResponse])
async def get_query_sting_advertisement(session: SessionDependancy,
                                        title: str = Query(None),
                                        description: str = Query(None),
                                        price: float = Query(None),
                                        owner: str = Query(None)
                                        ):
    stmt = select(models.Advertisement)
    if title:
        stmt = stmt.where(models.Advertisement.title.ilike(f"%{title}%"))
    if description:
        stmt = stmt.where(models.Advertisement.description.ilike(f"%{description}%"))
    if price:
        stmt = stmt.where(models.Advertisement.price == price)
    if owner:
        stmt = stmt.where(models.Advertisement.owner == owner)
    result = await session.execute(stmt)
    ads = result.scalars().all()
    return ads

@app.delete("/advertisement/{ad_id}", tags=['Advertisement'], response_model=DeleteAdvertisementResponse)
async def delete_advertisement(ad_id: int, session: SessionDependancy):
    await crud.delete_item(session, ad_id)
    return {"status": "success"}