import json
import os
from typing import Dict, Any


'''
Útmutató a fájl függvényeinek a használatához

Új felhasználó hozzáadása:

new_user = {
    "id": 4,  # Egyedi felhasználó azonosító
    "name": "Szilvás Szabolcs",
    "email": "szabolcs@plumworld.com"
}

Felhasználó hozzáadása a JSON fájlhoz:

add_user(new_user)

Hozzáadunk egy új kosarat egy meglévő felhasználóhoz:

new_basket = {
    "id": 104,  # Egyedi kosár azonosító
    "user_id": 2,  # Az a felhasználó, akihez a kosár tartozik
    "items": []  # Kezdetben üres kosár
}

add_basket(new_basket)

Új termék hozzáadása egy felhasználó kosarához:

user_id = 2
new_item = {
    "item_id": 205,
    "name": "Szilva",
    "brand": "Stanley",
    "price": 7.99,
    "quantity": 3
}

Termék hozzáadása a kosárhoz:

add_item_to_basket(user_id, new_item)

Hogyan használd a fájlt?

Importáld a függvényeket a filehandler.py modulból:

from filehandler import (
    add_user,
    add_basket,
    add_item_to_basket,
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    # Ez a függvény megegyezik a filereader-ben lévővel
    if not os.path.exists(JSON_FILE_PATH):
        raise ValueError("A data.json fájl nem található!")
        
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError("A JSON fájl formátuma érvénytelen vagy sérült!")

def save_json(data: Dict[str, Any]) -> None:
    # A 'w' (write) mód felülírja a fájlt. 
    # Az ensure_ascii=False felel azért, hogy a magyar ékezetek (pl. á, é) helyesen jelenjenek meg.
    # Az indent=4 teszi szépen, ember számára is olvashatóvá a JSON formátumot.
    with open(JSON_FILE_PATH, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_user(user: Dict[str, Any]) -> None:
    data = load_json()
    
    # Ellenőrizzük, hogy az ID foglalt-e már
    for existing_user in data.setdefault("Users", []):
        if existing_user.get("id") == user.get("id"):
            raise ValueError(f"Már létezik felhasználó a megadott ({user.get('id')}) azonosítóval!")
            
    # Ha minden rendben, hozzáadjuk a listához és mentjük
    data["Users"].append(user)
    save_json(data)

def add_basket(basket: Dict[str, Any]) -> None:
    data = load_json()
    
    # 1. Ellenőrizzük, hogy a kosár ID foglalt-e már
    for existing_basket in data.setdefault("Baskets", []):
        if existing_basket.get("id") == basket.get("id"):
            raise ValueError(f"Már létezik kosár a megadott ({basket.get('id')}) azonosítóval!")
            
    # 2. Ellenőrizzük, hogy létezik-e egyáltalán az a felhasználó, akihez rendelni akarjuk
    user_exists = any(u.get("id") == basket.get("user_id") for u in data.setdefault("Users", []))
    if not user_exists:
        raise ValueError(f"Nem létezik felhasználó a megadott ({basket.get('user_id')}) azonosítóval!")
        
    # Ha minden rendben, hozzáadjuk a listához és mentjük
    data["Baskets"].append(basket)
    save_json(data)

def add_item_to_basket(user_id: int, item: Dict[str, Any]) -> None:
    data = load_json()
    basket_found = False
    
    # Megkeressük a felhasználóhoz tartozó kosarat
    for basket in data.setdefault("Baskets", []):
        if basket.get("user_id") == user_id:
            # Ha megtaláltuk, hozzáadjuk a terméket a kosár 'items' listájához
            basket.setdefault("items", []).append(item)
            basket_found = True
            break # Kilépünk a ciklusból, hiszen megvan a kosár
            
    if not basket_found:
        raise ValueError(f"A megadott ({user_id}) azonosítójú felhasználónak nincs kosara! Előbb hozz létre egyet.")
        
    save_json(data)