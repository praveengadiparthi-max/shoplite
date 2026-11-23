import { useEffect, useState } from 'react'
import './App.css'

const PRODUCT_API = 'http://localhost:8001'
const ORDER_API = 'http://localhost:8002'

function App() {
  const [products, setProducts] = useState([])
  const [message, setMessage] = useState('')

  // Runs once when the page loads: fetch the product list
  useEffect(() => {
    fetch(`${PRODUCT_API}/products`)
      .then((res) => res.json())
      .then((data) => setProducts(data))
      .catch(() => setMessage('Could not load products'))
  }, [])

  // Runs when you click "Order"
  function placeOrder(productId) {
    fetch(`${ORDER_API}/orders`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_id: productId, quantity: 1 }),
    })
      .then((res) => res.json())
      .then((order) => setMessage(`Order #${order.id} placed: ${order.product_name}, total $${order.total}`))
      .catch(() => setMessage('Order failed'))
  }

  return (
    <div style={{ padding: 24, fontFamily: 'sans-serif' }}>
      <h1>Shoplite</h1>
      {message && <p><b>{message}</b></p>}
      <ul>
        {products.map((p) => (
          <li key={p.id} style={{ marginBottom: 8 }}>
            {p.name} — ${p.price}{' '}
            <button onClick={() => placeOrder(p.id)}>Order</button>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App