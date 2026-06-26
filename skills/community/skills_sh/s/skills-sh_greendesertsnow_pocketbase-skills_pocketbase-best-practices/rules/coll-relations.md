---
title: Configure Relations with Proper Cascade Options
impact: CRITICAL
impactDescription: Maintains referential integrity, prevents orphaned records, controls deletion behavior
tags: collections, relations, foreign-keys, cascade, design
---

## Configure Relations with Proper Cascade Options

Relation fields connect collections together. Proper cascade configuration ensures data integrity when referenced records are deleted.

**Incorrect (default cascade behavior not considered):**

```javascript
// Relation without considering deletion behavior
const ordersSchema = [
  { name: 'customer', type: 'relation', options: {
    collectionId: 'customers_collection_id',
    maxSelect: 1
    // No cascade options specified - defaults may cause issues
  }},
  { name: 'products', type: 'relation', options: {
    collectionId: 'products_collection_id'
    // Multiple products, no cascade handling
  }}
];

// Deleting a customer may fail or orphan orders
await pb.collection('customers').delete(customerId);
// Error: record is referenced by other records
```

**Correct (explicit cascade configuration):**

```javascript
// Carefully configured relations
const ordersSchema = [
  {
    name: 'customer',
    type: 'relation',
    required: true,
    options: {
      collectionId: 'customers_collection_id',
      maxSelect: 1,
      cascadeDelete: false  // Prevent accidental mass deletion
    }
  },
  {
    name: 'products',
    type: 'relation',
    options: {
      collectionId: 'products_collection_id',
      maxSelect: 99,
      cascadeDelete: false
    }
  }
];

// For dependent data like comments - cascade delete makes sense
const commentsSchema = [
  {
    name: 'post',
    type: 'relation',
    options: {
      collectionId: 'posts_collection_id',
      maxSelect: 1,
      cascadeDelete: true  // Delete comments when post is deleted
    }
  }
];
// NOTE: For audit logs, avoid cascadeDelete - logs should be retained
// for compliance/forensics even after the referenced user is deleted.
// Use cascadeDelete: false and handle user deletion separately.

// Handle deletion manually when cascade is false
try {
  await pb.collection('customers').delete(customerId);
} catch (e) {
  if (e.status === 400) {
    // Customer has orders - handle appropriately
    // Option 1: Soft delete (set 'deleted' flag)
    // Option 2: Reassign orders
    // Option 3: Delete orders first
  }
}
```

**Cascade options:**
- `cascadeDelete: true` - Delete referencing records when referenced record is deleted
- `cascadeDelete: false` - Block deletion if references exist (default for required relations)

**Best practices:**
- Use `cascadeDelete: true` for dependent data (comments on posts, logs for users)
- Use `cascadeDelete: false` for important data (orders, transactions)
- Consider soft deletes for audit trails
- Document your cascade strategy

Reference: [PocketBase Relations](https://pocketbase.io/docs/collections/#relation)
