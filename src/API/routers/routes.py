from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from schemas.schema import User, Basket, Item
from typing import List

# Importáljuk a korábban megírt segédfüggvényeket
from data.filehandler import add_user, add_basket, add_item_to_basket, save_json, load_json
from data.filereader import (
    get_user_by_id, 
    get_basket_by_user_id, 
    get_all_users, 
    get_total_price_of_basket
)

routers = APIRouter()

@routers.post('/adduser', response_model=User)
def adduser(user: User):
    try:
        # Pydantic objektum konvertálása szótárrá a mentéshez
        user_dict = user.model_dump()
        add_user(user_dict)
        return JSONResponse(status_code=201, content=user_dict)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Szerverhiba: {str(e)}")

@routers.post('/addshoppingbag')
def addshoppingbag(userid: int) -> str:
    try:
        # Új kosár objektum létrehozása (egyedi ID generálásával)
        data = load_json()
        existing_baskets = data.get("Baskets", [])
        new_id = max([b.get("id", 100) for b in existing_baskets], default=100) + 1
        
        new_basket = {
            "id": new_id,
            "user_id": userid,
            "items": []
        }
        add_basket(new_basket)
        return JSONResponse(status_code=201, content="Sikeres kosár hozzárendelés.")
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post('/additem', response_model=Basket)
def additem(userid: int, item: Item) -> Basket:
    try:
        item_dict = item.model_dump()
        add_item_to_basket(userid, item_dict)
        # Visszaadjuk a teljes kosarat a módosítás után
        data = load_json()
        basket = next((b for b in data["Baskets"] if b["user_id"] == userid), None)
        return JSONResponse(status_code=201, content=basket)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.put('/updateitem', response_model=Basket)
def updateitem(userid: int, itemid: int, updateItem: Item) -> Basket:
    try:
        data = load_json()
        basket = next((b for b in data["Baskets"] if b["user_id"] == userid), None)
        if not basket:
            raise ValueError("Nincs kosár ehhez a felhasználóhoz.")
        
        # Keressük meg a terméket és frissítsük
        found = False
        for i, item in enumerate(basket["items"]):
            if item["item_id"] == itemid:
                basket["items"][i] = updateItem.model_dump()
                found = True
                break
        
        if not found:
            raise ValueError("A termék nem található a kosárban.")
        
        save_json(data)
        return JSONResponse(status_code=200, content=basket)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@routers.delete('/deleteitem', response_model=Basket)
def deleteitem(userid: int, itemid: int) -> Basket:
    try:
        data = load_json()
        basket = next((b for b in data["Baskets"] if b["user_id"] == userid), None)
        if not basket:
            raise ValueError("Kosár nem található.")
        
        basket["items"] = [i for i in basket["items"] if i["item_id"] != itemid]
        save_json(data)
        return JSONResponse(status_code=200, content=basket)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@routers.get('/user', response_model=User)
def user(userid: int) -> User:
    try:
        res = get_user_by_id(userid)
        return JSONResponse(status_code=200, content=res)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@routers.get('/users', response_model=List[User])
def users() -> List[User]:
    try:
        res = get_all_users()
        return JSONResponse(status_code=200, content=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.get('/shoppingbag', response_model=List[Item])
def shoppingbag(userid: int) -> List[Item]:
    try:
        res = get_basket_by_user_id(userid)
        return JSONResponse(status_code=200, content=res)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

@routers.get('/getusertotal')
def getusertotal(userid: int) -> float:
    try:
        res = get_total_price_of_basket(userid)
        return JSONResponse(status_code=200, content={"total": res})
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))

# PDF 5. oldal szerinti extra endpointok: mentés és visszatöltés
@routers.post('/save')
def save(source: str, dest: str):
    try:
        # Itt egy egyszerű fájl másolást vagy JSON mentést valósítunk meg
        with open(source, "r", encoding="utf-8") as s:
            content = json.load(s)
        with open(dest, "w", encoding="utf-8") as d:
            json.dump(content, d, ensure_ascii=False, indent=4)
        return JSONResponse(status_code=200, content="Sikeres mentés.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@routers.post('/reload')
def reload(dest: str, source: str):
    # Logikája megegyezik a mentéssel, csak az irány fordított
    return save(source, dest)