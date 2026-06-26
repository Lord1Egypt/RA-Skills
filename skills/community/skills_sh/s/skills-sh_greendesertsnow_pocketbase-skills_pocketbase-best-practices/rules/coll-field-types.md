---
title: Choose Appropriate Field Types for Your Data
impact: CRITICAL
impactDescription: Prevents data corruption, improves query performance, reduces storage
tags: collections, schema, field-types, design
---

## Choose Appropriate Field Types for Your Data

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
