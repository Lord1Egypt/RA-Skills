---
title: Use View Collections for Complex Read-Only Queries
impact: HIGH
impactDescription: Simplifies complex queries, improves maintainability, enables aggregations
tags: collections, views, sql, aggregation, design
---

## Use View Collections for Complex Read-Only Queries

View collections execute custom SQL queries and expose results through the standard API. They're ideal for aggregations, joins, and computed fields without duplicating logic across your application.

**Incorrect (computing aggregations client-side):**

```javascript
// Fetching all records to compute stats client-side
const orders = await pb.collection('orders').getFullList();
const products = await pb.collection('products').getFullList();

// Expensive client-side computation
const stats = orders.reduce((acc, order) => {
  const product = products.find(p => p.id === order.product);
  acc.totalRevenue += order.quantity * product.price;
  acc.orderCount++;
  return acc;
}, { totalRevenue: 0, orderCount: 0 });
// Fetches all data, slow, memory-intensive
```

**Correct (using view collection):**

```javascript
// Create a view collection in PocketBase Admin UI or via API
// View SQL:
// SELECT
//   p.id,
//   p.name,
//   COUNT(o.id) as order_count,
//   SUM(o.quantity) as total_sold,
//   SUM(o.quantity * p.price) as revenue
// FROM products p
// LEFT JOIN orders o ON o.product = p.id
// GROUP BY p.id

// Simple, efficient query
const productStats = await pb.collection('product_stats').getList(1, 20, {
  sort: '-revenue'
});

// Each record has computed fields
productStats.items.forEach(stat => {
  console.log(`${stat.name}: ${stat.order_count} orders, $${stat.revenue}`);
});
```

**View collection use cases:**
- Aggregations (COUNT, SUM, AVG)
- Joining data from multiple collections
- Computed/derived fields
- Denormalized read models
- Dashboard statistics

**Limitations:**
- Read-only (no create/update/delete)
- Must return `id` column
- No realtime subscriptions
- API rules still apply for access control

Reference: [PocketBase View Collections](https://pocketbase.io/docs/collections/#view-collection)
