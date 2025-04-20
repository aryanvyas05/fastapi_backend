from pydantic import BaseModel

class Store(BaseModel):
    sId: int
    Sname: str
    Street: str
    City: str
    StateAb: str
    Zipcode: str
    Sdate: str
    Telno: str
    SURL: str

class Vendor(BaseModel):
    vId: int
    Vname: str
    Street: str
    City: str
    StateAb: str
    Zipcode: str

class Item(BaseModel):
    iId: int
    iName: str
    sPrice: float
    category: str

class VendorItemLink(BaseModel):
    vId: int
    iId: int

class StoreItemLink(BaseModel):
    sId: int
    iId: int
    quantity: int
