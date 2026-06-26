---
title: Use getFirstListItem for Single Record Lookups
impact: MEDIUM
impactDescription: Cleaner code, automatic error handling for not found
tags: query, lookup, find, getFirstListItem
---

## Use getFirstListItem for Single Record Lookups

Use `getFirstListItem()` when you need to find a single record by a field value other than ID. It's cleaner than `getList()` with limit 1 and provides proper error handling.

**Incorrect (manual single-record lookup):**

```javascript
// Using getList with limit 1 - verbose
async function findUserByEmail(email) {
  const result = await pb.collection('users').getList(1, 1, {
    filter: pb.filter('email = {:email}', { email })
  });

  if (result.items.length === 0) {
    throw new Error('User not found');
  }

  return result.items[0];
}

// Using getFullList then filtering - wasteful
async function findUserByUsername(username) {
  const users = await pb.collection('users').getFullList({
    filter: pb.filter('username = {:username}', { username })
  });
  return users[0];  // Might be undefined!
}

// Fetching by ID when you have a different identifier
async function findProductBySku(sku) {
  // Wrong: getOne expects the record ID
  const product = await pb.collection('products').getOne(sku);  // Fails!
}
```

**Correct (using getFirstListItem):**

```javascript
// Clean single-record lookup by any field
async function findUserByEmail(email) {
  try {
    const user = await pb.collection('users').getFirstListItem(
      pb.filter('email = {:email}', { email })
    );
    return user;
  } catch (error) {
    if (error.status === 404) {
      return null;  // Not found
    }
    throw error;
  }
}

// Lookup by unique field
async function findProductBySku(sku) {
  return pb.collection('products').getFirstListItem(
    pb.filter('sku = {:sku}', { sku })
  );
}

// Lookup with expand
async function findOrderByNumber(orderNumber) {
  return pb.collection('orders').getFirstListItem(
    pb.filter('orderNumber = {:num}', { num: orderNumber }),
    { expand: 'customer,items' }
  );
}

// Complex filter conditions
async function findActiveSubscription(userId) {
  return pb.collection('subscriptions').getFirstListItem(
    pb.filter(
      'user = {:userId} && status = "active" && expiresAt > @now',
      { userId }
    )
  );
}

// With field selection
async function getUserIdByEmail(email) {
  const user = await pb.collection('users').getFirstListItem(
    pb.filter('email = {:email}', { email }),
    { fields: 'id' }
  );
  return user.id;
}
```

**Comparison with getOne:**

```javascript
// getOne - fetch by record ID
const post = await pb.collection('posts').getOne('abc123');

// getFirstListItem - fetch by any filter (use pb.filter for safe binding)
const post = await pb.collection('posts').getFirstListItem(
  pb.filter('slug = {:slug}', { slug: 'hello-world' })
);
const user = await pb.collection('users').getFirstListItem(
  pb.filter('username = {:name}', { name: 'john' })
);
const order = await pb.collection('orders').getFirstListItem(
  pb.filter('orderNumber = {:num}', { num: 12345 })
);
```

**Error handling:**

```javascript
// getFirstListItem throws 404 if no match found
try {
  const user = await pb.collection('users').getFirstListItem(
    pb.filter('email = {:email}', { email })
  );
  return user;
} catch (error) {
  if (error.status === 404) {
    // No matching record - handle appropriately
    return null;
  }
  // Other error (network, auth, etc.)
  throw error;
}

// Wrapper function for optional lookup
async function findFirst(collection, filter, options = {}) {
  try {
    return await pb.collection(collection).getFirstListItem(filter, options);
  } catch (error) {
    if (error.status === 404) return null;
    throw error;
  }
}

// Usage
const user = await findFirst('users', pb.filter('email = {:e}', { e: email }));
if (!user) {
  console.log('User not found');
}
```

**When to use each method:**

| Method | Use When |
|--------|----------|
| `getOne(id)` | You have the record ID |
| `getFirstListItem(filter)` | Finding by unique field (email, slug, sku) |
| `getList(1, 1, { filter })` | Need pagination metadata |
| `getFullList({ filter })` | Expecting multiple results |

Reference: [PocketBase Records API](https://pocketbase.io/docs/api-records/)
