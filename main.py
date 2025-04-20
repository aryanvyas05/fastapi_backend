from fastapi import FastAPI, Body, Path
from fastapi.responses import JSONResponse
from models import Store, Vendor, Item, VendorItemLink, StoreItemLink
from database import get_connection

app = FastAPI()
@app.get("/")
def home():
    return {"message": "FastAPI is running!"}

@app.post("/store")
def create_store(store: Store = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO store ("sId", "Sname", "Street", "City", "StateAb", "Zipcode")
    VALUES (%s, %s, %s, %s, %s, %s)
    """,
    (store.sId, store.Sname, store.Street, store.City, store.StateAb, store.Zipcode),
    )


    conn.commit()
    conn.close()
    return {"message": "Store added successfully"}


@app.post("/vendor")
def create_vendor(vendor: Vendor = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
    'INSERT INTO vendor ("vId", "Vname", "Street", "City", "StateAb", "Zipcode") VALUES (%s, %s, %s, %s, %s, %s)',
        (vendor.vId, vendor.Vname, vendor.Street, vendor.City, vendor.StateAb, vendor.Zipcode)
    )

    conn.commit()
    conn.close()
    return {"message": "Vendor added successfully"}

@app.post("/Item")
def create_item(item: Item = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        'INSERT INTO item ("iId", "Iname", "Sprice", "Category") VALUES (%s, %s, %s, %s)',
        (item.iId, item.iName, item.sPrice, item.category)
    )
    conn.commit()
    conn.close()
    return {"message": "Item added successfully"}

@app.post("/vendor-item")
def link_vendor_item(link: VendorItemLink = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO vendor_item ("vId", "iId") VALUES (%s, %s)',
        (link.vId, link.iId)
    )

    conn.commit()
    conn.close()
    return {"message": "Vendor linked to item successfully"}

@app.post("/store-item")
def link_store_item(link: StoreItemLink = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO store_item ("sId", "iId", "Scount") VALUES (%s, %s, %s)',
        (link.sId, link.iId, link.quantity)
    )

    conn.commit()
    conn.close()
    return {"message": "Item added to store invetory successfully"}

@app.get("/products")
def get_products():
    try:
        conn = get_connection()
        cursor = conn.cursor()
    
        cursor.execute("""
            SELECT i."iId", i."Iname", i."Sprice", i."Category", COALESCE(si."Scount", 0)
            FROM item i
            LEFT JOIN store_item si ON i."iId" = si."iId"
            WHERE si."sId" = 1
        """)
    
        rows = cursor.fetchall()
        conn.close()
    
        products = [
            {
                "iId": row[0],
                "iName": row[1],
                "sPrice": float(row[2]),
                "category": row[3],
                "quantity": row[4]
            }
            for row in rows
        ]

        return JSONResponse(content=products)
    except Exception as e:
    # Handle any exception
        print(f"An error occurred: {e}")
@app.put("/products/{iId}")
def update_product(iId: int = Path(...), updated_item: Item = Body(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE item
        SET "Iname" = %s, "Sprice" = %s, "Category" = %s
        WHERE "iId" = %s
    """, (updated_item.iName, updated_item.sPrice, updated_item.category, iId))

    conn.commit()
    conn.close()

    return {"message": "Item updated successfully"}
@app.delete("/products/{iId}")
def delete_product(iId: int = Path(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT "vId" FROM vendor_item WHERE "iId" = %s', (iId,))
    vId_result = cursor.fetchone()
    vId = vId_result[0] if vId_result else None

    cursor.execute('DELETE FROM store_item WHERE "iId" = %s', (iId,))
    cursor.execute('DELETE FROM vendor_item WHERE "iId" = %s', (iId,))
    cursor.execute('DELETE FROM item WHERE "iId" = %s', (iId,))

    if vId:
        cursor.execute('SELECT COUNT(*) FROM vendor_item WHERE "vId" = %s', (vId,))
        if cursor.fetchone()[0] == 0:
            cursor.execute('DELETE FROM vendor WHERE "vId" = %s', (vId,))

    conn.commit()
    conn.close()

    return {"message": "Item and vendor cleaned up successfully"}
