from fastapi import FastAPI,Path,Query,HTTPException,status, Request, Header
from typing import Optional
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app=FastAPI()


templates = Jinja2Templates(directory="templates")


class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str]=None

class UpdateItem(BaseModel):
    name: Optional[str]=None
    price: Optional[float] =None
    brand: Optional[str]=None

inventory ={}

#今後會使用該代碼來進行改寫

@app.get("/git-item/{item_id}")
def get_item(item_id: int=Path(None,description="We can't find this id",gt=0)):
    return inventory[item_id]


@app.get("/git-by-name")
def get_item(name: str = Query(None, title="name", description="Name of item.", max_length=10, min_length=2)):
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise HTTPException(status_code=404, detail="Item name not find.")

@app.post("/create-item")
def create_item(item_id:int,item:UpdateItem):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Item ID already exists.")

    inventory[item_id]=item
    return inventory[item_id]

@app.put("/update-item/{item_id}")
def update_item(item_id:int ,item:Item):
    if item_id not in inventory:
         raise HTTPException(status_code=404, detail="Item ID does not exists.")

    if item.name != None:
        inventory[item_id].name=item.name
       
    if item.price != None:
        inventory[item_id].price=item.price
       
    if item.brand != None:
        inventory[item_id].brand=item.brand

    return inventory[item_id]

@app.delete("/detele-item")
def delete_item(item_id: int = Query(...,description="DELETE!",gt=0)):
    if item_id not in inventory:
       raise HTTPException(status_code=404, detail="Item ID does not exists.")

    del inventory[item_id]
    return {"Success":"Item deleted!"}