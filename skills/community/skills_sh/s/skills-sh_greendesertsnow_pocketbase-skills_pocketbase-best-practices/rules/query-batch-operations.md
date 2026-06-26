---
title: Use Batch Operations for Multiple Writes
impact: HIGH
impactDescription: Atomic transactions, 10x fewer API calls, consistent state
tags: query, batch, transactions, performance
---

## Use Batch Operations for Multiple Writes

Batch operations combine multiple create/update/delete operations into a single atomic transaction. This ensures consistency and dramatically reduces API calls.

**Incorrect (individual requests):**

```javascript
// Creating multiple records individually
async function createOrderWithItems(order, items) {
  // If any fails, partial data remains!
  const createdOrder = await pb.collection('orders').create(order);

  for (const item of items) {
    await pb.collection('order_items').create({
      ...item,
      order: createdOrder.id
    });
  }
  // 1 + N API calls, not atomic
}

// Updating multiple records
async function updatePrices(products) {
  for (const product of products) {
    await pb.collection('products').update(product.id, {
      price: product.newPrice
    });
  }
  // N API calls, some might fail leaving inconsistent state
}

// Mixed operations
async function transferFunds(fromId, toId, amount) {
  // NOT ATOMIC - can leave invalid state!
  await pb.collection('accounts').update(fromId, { 'balance-': amount });
  // If this fails, money disappears!
  await pb.collection('accounts').update(toId, { 'balance+': amount });
}
```

**Correct (using batch operations):**

```javascript
// Atomic batch create
async function createOrderWithItems(order, items) {
  const batch = pb.createBatch();

  // Pre-generate order ID so items can reference it in the same batch
  // PocketBase accepts custom IDs (15-char alphanumeric)
  const orderId = crypto.randomUUID().replaceAll('-', '').slice(0, 15);

  // Queue order creation with known ID
  batch.collection('orders').create({ ...order, id: orderId });

  // Queue all items referencing the pre-generated order ID
  items.forEach(item => {
    batch.collection('order_items').create({
      ...item,
      order: orderId
    });
  });

  // Execute atomically
  const results = await batch.send();
  // All succeed or all fail together

  return {
    order: results[0],
    items: results.slice(1)
  };
}

// Batch updates
async function updatePrices(products) {
  const batch = pb.createBatch();

  products.forEach(product => {
    batch.collection('products').update(product.id, {
      price: product.newPrice
    });
  });

  const results = await batch.send();
  // 1 API call, atomic
  return results;
}

// Batch upsert (create or update)
async function syncProducts(products) {
  const batch = pb.createBatch();

  products.forEach(product => {
    batch.collection('products').upsert({
      id: product.sku,  // Use SKU as ID for upsert matching
      name: product.name,
      price: product.price,
      stock: product.stock
    });
  });

  return batch.send();
}

// Mixed operations in transaction
// NOTE: Batch operations respect API rules per-operation, but ensure your
// business logic validates inputs (e.g., sufficient balance) server-side
// via hooks or API rules to prevent unauthorized transfers.
async function transferFunds(fromId, toId, amount) {
  const batch = pb.createBatch();

  batch.collection('accounts').update(fromId, { 'balance-': amount });
  batch.collection('accounts').update(toId, { 'balance+': amount });

  // Create audit record
  batch.collection('transfers').create({
    from: fromId,
    to: toId,
    amount,
    timestamp: new Date()
  });

  // All three operations atomic
  const [fromAccount, toAccount, transfer] = await batch.send();
  return { fromAccount, toAccount, transfer };
}

// Batch delete
async function deletePostWithComments(postId) {
  // First get comment IDs
  const comments = await pb.collection('comments').getFullList({
    filter: pb.filter('post = {:postId}', { postId }),
    fields: 'id'
  });

  const batch = pb.createBatch();

  // Queue all deletions
  comments.forEach(comment => {
    batch.collection('comments').delete(comment.id);
  });
  batch.collection('posts').delete(postId);

  await batch.send();
  // Post and all comments deleted atomically
}
```

**Batch operation limits:**
- **Must be enabled first** in Dashboard > Settings > Application (disabled by default; returns 403 otherwise)
- Operations execute in a single database transaction
- All succeed or all rollback
- Respects API rules for each operation
- Configurable limits: `maxRequests`, `timeout`, and `maxBodySize` (set in Dashboard)
- **Avoid large file uploads** in batches over slow networks -- they block the entire transaction
- Avoid custom hooks that call slow external APIs within batch operations

**When to use batch:**

| Scenario | Use Batch? |
|----------|-----------|
| Creating parent + children | Yes |
| Bulk import/update | Yes |
| Financial transactions | Yes |
| Single record operations | No |
| Independent operations | Optional |

Reference: [PocketBase Batch API](https://pocketbase.io/docs/api-records/#batch-operations)
