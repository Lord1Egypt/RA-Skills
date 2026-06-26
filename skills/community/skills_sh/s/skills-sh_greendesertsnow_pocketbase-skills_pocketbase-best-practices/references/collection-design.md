# Collection Design

**Impact: CRITICAL**

Schema design, field types, relations, indexes, and collection type selection. Foundation for application architecture and long-term maintainability.

---

## 1. Use Auth Collections for User Accounts

**Impact: CRITICAL (Built-in authentication, password hashing, OAuth2 support)**

Auth collections provide built-in authentication features including secure password hashing, email verification, OAuth2 support, and token management. Using base collections for users requires reimplementing these security-critical features.

**Incorrect (using base collection for users):**

```javascript
// Base collection loses all auth features
const usersCollection = {
  name: 'users',
  type: 'base',  // Wrong! No auth capabilities
  schema: [
    { name: 'email', type: 'email' },
    { name: 'password', type: 'text' },  // Stored in plain text!
    { name: 'name', type: 'text' }
  ]
};

// Manual login implementation - insecure
const user = await pb.collection('users').getFirstListItem(
  `email = "${email}" && password = "${password}"`  // SQL injection risk!
);
```

**Correct (using auth collection):**

```javascript
// Auth collection with built-in security
const usersCollection = {
  name: 'users',
  type: 'auth',  // Enables authentication features
  schema: [
    { name: 'name', type: 'text' },
    { name: 'avatar', type: 'file', options: { maxSelect: 1 } }
  ],
  options: {
    allowEmailAuth: true,
    allowOAuth2Auth: true,
    requireEmail: true,
    minPasswordLength: 8
  }
};

// Secure authentication with password hashing
const authData = await pb.collection('users').authWithPassword(
  'user@example.com',
  'securePassword123'
);

// Token automatically stored in authStore
// NOTE: Never log tokens in production - shown here for illustration only
console.log('Authenticated as:', pb.authStore.record.id);
```

**When to use each type:**
- **Auth collection**: User accounts, admin accounts, any entity that needs to log in
- **Base collection**: Regular data like posts, products, orders, comments
- **View collection**: Read-only aggregations or complex queries

Reference: [PocketBase Auth Collections](https://pocketbase.io/docs/collections/#auth-collection)

## 2. Choose Appropriate Field Types for Your Data

**Impact: CRITICAL (Prevents data corruption, improves query performance, reduces storage)**

Selecting the wrong field type leads to data validation issues, wasted storage, and poor query performance. PocketBase provides specialized field types that enforce constraints at the database level.

**Incorrect (using text for everything):**

```javascript
// Using plain text fields for structured data
const collection = {
  name: 'products',
  schema: [
    { name: 'price', type: 'text' },      // Should be number
    { name: 'email', type: 'text' },       // Should be email
    { name: 'website', type: 'text' },     // Should be url
    { name: 'active', type: 'text' },      // Should be bool
    { name: 'tags', type: 'text' },        // Should be select or json
    { name: 'created', type: 'text' }      // Should be autodate
  ]
};
// No validation, inconsistent data, manual parsing required
```

**Correct (using appropriate field types):**

```javascript
// Using specialized field types with proper validation
const collection = {
  name: 'products',
  type: 'base',
  schema: [
    { name: 'price', type: 'number', options: { min: 0 } },
    { name: 'email', type: 'email' },
    { name: 'website', type: 'url' },
    { name: 'active', type: 'bool' },
    { name: 'tags', type: 'select', options: {
      maxSelect: 5,
      values: ['electronics', 'clothing', 'food', 'other']
    }},
    { name: 'metadata', type: 'json' }
    // created/updated are automatic system fields
  ]
};
// Built-in validation, proper indexing, type-safe queries
```

**Available field types:**
- `text` - Plain text with optional min/max length, regex pattern
- `number` - Integer or decimal with optional min/max
- `bool` - True/false values
- `email` - Email with format validation
- `url` - URL with format validation
- `date` - Date/datetime values
- `autodate` - Auto-set on create/update
- `select` - Single or multi-select from predefined values
- `json` - Arbitrary JSON data
- `file` - File attachments
- `relation` - References to other collections
- `editor` - Rich text HTML content

Reference: [PocketBase Collections](https://pocketbase.io/docs/collections/)

## 3. Use GeoPoint Fields for Location Data

**Impact: MEDIUM (Built-in geographic queries, distance calculations)**

PocketBase provides a dedicated GeoPoint field type for storing geographic coordinates with built-in distance query support via `geoDistance()`.

**Incorrect (storing coordinates as separate fields):**

```javascript
// Separate lat/lon fields - no built-in distance queries
const placesSchema = [
  { name: 'name', type: 'text' },
  { name: 'latitude', type: 'number' },
  { name: 'longitude', type: 'number' }
];

// Manual distance calculation - complex and slow
async function findNearby(lat, lon, maxKm) {
  const places = await pb.collection('places').getFullList();

  // Calculate distance for every record client-side
  return places.filter(place => {
    const dist = haversine(lat, lon, place.latitude, place.longitude);
    return dist <= maxKm;
  });
}
```

**Correct (using GeoPoint field):**

```javascript
// GeoPoint field stores coordinates as { lon, lat } object
const placesSchema = [
  { name: 'name', type: 'text' },
  { name: 'location', type: 'geopoint' }
];

// Creating a record with GeoPoint
await pb.collection('places').create({
  name: 'Coffee Shop',
  location: { lon: -73.9857, lat: 40.7484 }  // Note: lon first!
});

// Or using "lon,lat" string format
await pb.collection('places').create({
  name: 'Restaurant',
  location: '-73.9857,40.7484'  // String format also works
});

// Query nearby locations using geoDistance()
async function findNearby(lon, lat, maxKm) {
  // geoDistance returns distance in kilometers
  const places = await pb.collection('places').getList(1, 50, {
    filter: pb.filter(
      'geoDistance(location, {:point}) <= {:maxKm}',
      {
        point: { lon, lat },
        maxKm: maxKm
      }
    ),
    sort: pb.filter('geoDistance(location, {:point})', { point: { lon, lat } })
  });

  return places;
}

// Find places within 5km of Times Square
const nearbyPlaces = await findNearby(-73.9857, 40.7580, 5);

// Use in API rules for location-based access
// listRule: geoDistance(location, @request.query.point) <= 10
```

**geoDistance() function:**

```javascript
// Syntax: geoDistance(geopointField, referencePoint)
// Returns: distance in kilometers

// In filter expressions
filter: 'geoDistance(location, "-73.9857,40.7484") <= 5'

// With parameter binding (recommended)
filter: pb.filter('geoDistance(location, {:center}) <= {:radius}', {
  center: { lon: -73.9857, lat: 40.7484 },
  radius: 5
})

// Sorting by distance
sort: 'geoDistance(location, "-73.9857,40.7484")'  // Closest first
sort: '-geoDistance(location, "-73.9857,40.7484")' // Farthest first
```

**GeoPoint data format:**

```javascript
// Object format (recommended)
{ lon: -73.9857, lat: 40.7484 }

// String format
"-73.9857,40.7484"  // "lon,lat" order

// Important: longitude comes FIRST (GeoJSON convention)
```

**Use cases:**
- Store-locator / find nearby
- Delivery radius validation
- Geofencing in API rules
- Location-based search results

**Limitations:**
- Spherical Earth calculation (accurate to ~0.3%)
- No polygon/area containment queries
- Single point per field (use multiple fields for routes)

Reference: [PocketBase GeoPoint](https://pocketbase.io/docs/collections/#geopoint)

## 4. Create Indexes for Frequently Filtered Fields

**Impact: CRITICAL (10-100x faster queries on large collections)**

PocketBase uses SQLite which benefits significantly from proper indexing. Queries filtering or sorting on unindexed fields perform full table scans.

**Incorrect (no indexes on filtered fields):**

```javascript
// Querying without indexes
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'author = "user123" && status = "published"',
  sort: '-publishedAt'
});
// Full table scan on large collections - very slow

// API rules also query without indexes
// listRule: "author = @request.auth.id"
// Every list request scans entire table
```

**Correct (indexed fields):**

```javascript
// Create collection with indexes via Admin UI or migration
// In PocketBase Admin: Collection > Indexes > Add Index

// Common index patterns:
// 1. Single field index for equality filters
//    CREATE INDEX idx_posts_author ON posts(author)

// 2. Composite index for multiple filters
//    CREATE INDEX idx_posts_author_status ON posts(author, status)

// 3. Index with sort field
//    CREATE INDEX idx_posts_status_published ON posts(status, publishedAt DESC)

// Queries now use indexes
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'author = "user123" && status = "published"',
  sort: '-publishedAt'
});
// Index scan - fast even with millions of records

// For unique constraints (e.g., slug)
// CREATE UNIQUE INDEX idx_posts_slug ON posts(slug)
```

**Index recommendations:**
- Fields used in `filter` expressions
- Fields used in `sort` parameters
- Fields used in API rules (`listRule`, `viewRule`, etc.)
- Relation fields (automatically indexed)
- Unique fields like slugs or codes

**Index considerations for SQLite:**
- Composite indexes work left-to-right (order matters)
- Too many indexes slow down writes
- Use `EXPLAIN QUERY PLAN` in SQL to verify index usage
- Partial indexes for filtered subsets

```sql
-- Check if index is used
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author = 'user123' AND status = 'published';
-- Should show "USING INDEX" not "SCAN"
```

Reference: [SQLite Query Planning](https://www.sqlite.org/queryplanner.html)

## 5. Configure Relations with Proper Cascade Options

**Impact: CRITICAL (Maintains referential integrity, prevents orphaned records, controls deletion behavior)**

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

## 6. Use View Collections for Complex Read-Only Queries

**Impact: HIGH (Simplifies complex queries, improves maintainability, enables aggregations)**

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

