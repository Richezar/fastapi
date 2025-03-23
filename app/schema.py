from pydantic import BaseModel
from datetime import datetime
from typing import List

class CreateAdvertisementRequest(BaseModel):
    title: str
    description: str
    price: float
    owner: str

class CreateAdvertisementResponse(BaseModel):
    id: int

class UpdateAdvertisementRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    owner: str | None = None

class UpdateAdvertisementResponse(BaseModel):
    pass

class DeleteAdvertisementResponse(BaseModel):
    status: str

class GetAdvertisementResponse(BaseModel):
    id: int
    title: str
    description: str
    price: float
    owner: str
    date_created: datetime
