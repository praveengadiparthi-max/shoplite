import os

import httpx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://localhost:8001")

app = FastAPI(title="order-service")


class OrderRequest(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class Order(BaseModel):
    id: int
    product_id: int
    product_name: str
    quantity: int
    total: float


orders = []


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/orders")
def list_orders():
    return orders


@app.post("/orders", status_code=201)
def create_order(req: OrderRequest):
    url = f"{PRODUCT_SERVICE_URL}/products/{req.product_id}"
    try:
        resp = httpx.get(url, timeout=3.0)
    except httpx.RequestError:
        raise HTTPException(status_code=503, detail="product-service is unavailable")

    if resp.status_code == 404:
        raise HTTPException(status_code=404, detail="Product not found")

    product = resp.json()
    order = Order(
        id=len(orders) + 1,
        product_id=product["id"],
        product_name=product["name"],
        quantity=req.quantity,
        total=round(product["price"] * req.quantity, 2),
    )
    orders.append(order)
    return order