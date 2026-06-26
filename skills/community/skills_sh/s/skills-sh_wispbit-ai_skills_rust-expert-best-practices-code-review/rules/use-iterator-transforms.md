---
title: Use Iterator Transforms Instead of Push Loops
impact: MEDIUM-HIGH
impactDescription: Improves code clarity and functional programming style
tags: iterators, functional-programming, collections, idiomatic-rust, rust
---

## Use Iterator Transforms Instead of Push Loops

**Impact: MEDIUM-HIGH (Improves code clarity and functional programming style)**

Use iterator transforms instead of explicit push loops when building collections with simple transformations and filtering.

Replace `for` loops that iterate over a collection and push elements to a mutable `Vec` when the loop only contains simple filtering with `if` conditions and has no early breaks, continues, or returns.

**Iterator Methods to Use:**
- `.filter()` for conditional inclusion
- `.map()` for transformations
- `.filter_map()` for combined filtering and transformation
- `.collect()` to build the final collection

### BAD Examples

```rust
// Simple filtering and transformation
let mut names = Vec::new();
for user in users {
    if user.is_active {
        names.push(user.name.to_lowercase());
    }
}

// Just transformation
let mut ids = Vec::new();
for item in items {
    ids.push(item.id);
}

// Multiple conditions with filtering
let mut valid_emails = Vec::new();
for contact in contacts {
    if contact.email.is_some() && contact.verified {
        valid_emails.push(contact.email.unwrap());
    }
}

// Simple filtering without transformation
let mut active_users = Vec::new();
for user in users {
    if user.status == Status::Active {
        active_users.push(user);
    }
}
```

### GOOD Examples

```rust
// Iterator chain with filter and map
let names: Vec<_> = users
    .into_iter()
    .filter(|u| u.is_active)
    .map(|u| u.name.to_lowercase())
    .collect();

// Simple map transformation
let ids: Vec<_> = items.into_iter().map(|item| item.id).collect();

// Combined filtering and transformation with filter_map
let valid_emails: Vec<_> = contacts
    .into_iter()
    .filter_map(|c| if c.verified { c.email } else { None })
    .collect();

// Simple filtering
let active_users: Vec<_> = users
    .into_iter()
    .filter(|u| u.status == Status::Active)
    .collect();

// Complex logic that should remain as loop (has early return)
let mut results = Vec::new();
for item in items {
    if item.is_critical() {
        return Err("Critical item found");
    }
    if item.is_valid() {
        results.push(item.process());
    }
}
```