from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="product-service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Product(BaseModel):
    id: int
    name: str
    price: float


products = [
    Product(id=1, name="Keyboard", price=49.99),
    Product(id=2, name="Mouse", price=19.99),
    Product(id=3, name="Monitor", price=199.00),
]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/products")
def list_products():
    return products


@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")