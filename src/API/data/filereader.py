import json
import os
from typing import Dict, Any, List

'''
Útmutató a fájl használatához:

Felhasználó adatainak lekérdezése:

user_id = 1
user = get_user_by_id(user_id)
print(f"Felhasználó adatai: {user}")

Felhasználó kosarának tartalmának lekérdezése:

user_id = 1
basket = get_basket_by_user_id(user_id)
print(f"Felhasználó kosarának tartalma: {basket}")

Összes felhasználó lekérdezése:

users = get_all_users()
print(f"Összes felhasználó: {users}")

Felhasználó kosarában lévő termékek összárának lekérdezése:

user_id = 1
total_price = get_total_price_of_basket(user_id)
print(f"A felhasználó kosarának összára: {total_price}")

Hogyan futtasd?

Importáld a függvényeket a filehandler.py modulból:

from filereader import (
    get_user_by_id,
    get_basket_by_user_id,
    get_all_users,
    get_total_price_of_basket
)

 - Hiba esetén ValuErrort kell dobni, lehetőség szerint ezt a 
   kliens oldalon is jelezni kell.

'''

# A JSON fájl elérési útja
JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), "data.json")

def load_json() -> Dict[str, Any]:
    # Ellenőrizzük, hogy létezik-e egyáltalán a fájl
    if not os.path.exists(JSON_FILE_PATH):
        raise ValueError("A data.json fájl nem található!")
        
    with open(JSON_FILE_PATH, "r", encoding="utf-8") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            raise ValueError("A JSON fájl formátuma érvénytelen vagy sérült!")

def get_user_by_id(user_id: int) -> Dict[str, Any]:
    data = load_json()
    users = data.get("Users", [])
    
    for user in users:
        if user.get("id") == user_id:
            return user
            
    # Ha végigért a cikluson és nem találta meg
    raise ValueError(f"Nem található felhasználó a következő azonosítóval: {user_id}")

def get_basket_by_user_id(user_id: int) -> List[Dict[str, Any]]:
    # Először ellenőrizzük, hogy létezik-e a felhasználó (ha nem, ez dobja a ValueErrort)
    get_user_by_id(user_id)
    
    data = load_json()
    baskets = data.get("Baskets", [])
    
    for basket in baskets:
        if basket.get("user_id") == user_id:
            return basket.get("items", [])
            
    raise ValueError(f"A {user_id} azonosítójú felhasználóhoz nincs kosár rendelve!")

def get_all_users() -> List[Dict[str, Any]]:
    data = load_json()
    return data.get("Users", [])

def get_total_price_of_basket(user_id: int) -> float:
    # Lekérjük a kosár tartalmát (ha nincs, itt is ValueError-t kapunk)
    items = get_basket_by_user_id(user_id)
    
    total_price = 0.0
    for item in items:
        # Összeadjuk a termékek árát beszorozva a mennyiséggel
        price = item.get("price", 0.0)
        quantity = item.get("quantity", 0)
        total_price += price * quantity
        
    # Kerekítjük két tizedesjegyre a lebegőpontos pontatlanságok elkerülése miatt
    return round(total_price, 2)