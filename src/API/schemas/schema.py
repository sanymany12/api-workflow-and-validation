from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List
import re
'''

Útmutató a fájl használatához:

Az osztályokat a schema alapján ki kell dolgozni.

A schema.py az adatok küldésére és fogadására készített osztályokat tartalmazza.
Az osztályokban az adatok legyenek validálva.
 - az int adatok nem lehetnek negatívak.
 - az email mező csak e-mail formátumot fogadhat el.
 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

ShopName='WebShop'

class Item(BaseModel):
    item_id: int = Field(..., ge=0, description="A termék azonosítója nem lehet negatív")
    name: str 
    brand: str
    price: float = Field(..., ge=0.0, description="Az ár nem lehet negatív")
    quantity: int = Field(..., ge=0, description="A mennyiség nem lehet negatív")

class Basket(BaseModel):
    id: int = Field(..., ge=0, description="A kosár azonosítója nem lehet negatív")
    user_id: int = Field(..., ge=0, description="A felhasználó azonosítója nem lehet negatív")
    items: List[Item] = []

class User(BaseModel):
    id: int = Field(..., ge=0, description="A felhasználó azonosítója nem lehet negatív")
    name: str
    email: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(pattern, v):
            raise ValueError("Érvénytelen e-mail formátum!")
        return v
