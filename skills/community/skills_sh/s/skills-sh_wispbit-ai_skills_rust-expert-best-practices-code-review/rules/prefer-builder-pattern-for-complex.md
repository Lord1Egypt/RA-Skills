---
title: Prefer Builder Pattern for Complex Constructors
impact: HIGH
impactDescription: Improves API ergonomics and prevents parameter confusion
tags: builder-pattern, api-design, constructors, ergonomics, rust
---

## Prefer Builder Pattern for Complex Constructors

**Impact: HIGH (Improves API ergonomics and prevents parameter confusion)**

Rust constructors with multiple parameters (especially with optional values) should use the builder pattern instead of having many parameters.

**Constructors that should use builder pattern:**

- Functions with 4 or more parameters
- Functions with `Option<T>` parameters (regardless of parameter count)
- Functions where parameter order could be confusing

**Exclude from builder pattern:**

- Simple constructors with 1-3 required parameters only
- Structs/impls already ending with "Builder"
- Copy/Clone operations (`from_existing`, `from_other`, etc.)
- Internal utility constructors

### BAD Examples

```rust
// Too many parameters, hard to remember order
fn create_entity(
    field_a: String,
    field_b: String,
    field_c: u8,
    flag_a: bool,
    flag_b: bool,
    limit: u32,
    optional_field: Option<String>,
) -> Entity {
    Entity {
        field_a,
        field_b,
        field_c,
        flag_a,
        flag_b,
        limit,
        optional_field,
    }
}

// Constructor with optional parameters
impl ServiceConnection {
    fn new(
        endpoint: String,
        port: u16,
        user_id: String,
        secret: Option<String>,
        use_tls: Option<bool>,
    ) -> Self {
        Self {
            endpoint,
            port,
            user_id,
            secret,
            use_tls: use_tls.unwrap_or(false),
        }
    }
}

// Constructor with exactly 4 parameters
impl CatalogRecord {
    fn new(
        record_id: RecordId,
        label: String,
        tags: Vec<RecordTag>,
        notes: Option<String>,
    ) -> Self {
        Self {
            record_id,
            label,
            tags,
            notes,
        }
    }
}
```

### GOOD Examples

```rust
// Simple constructor - no builder needed
impl Vector2 {
    fn new(x: f64, y: f64) -> Self {
        Self { x, y }
    }
}

// Already using builder pattern
impl EntityBuilder {
    fn new() -> Self {
        Self {
            field_a: String::new(),
            field_b: String::new(),
            field_c: 0,
            flag_a: false,
            flag_b: false,
            limit: 100,
            optional_field: None,
        }
    }

    fn field_a(mut self, value: String) -> Self {
        self.field_a = value;
        self
    }

    fn field_b(mut self, value: String) -> Self {
        self.field_b = value;
        self
    }

    fn build(self) -> Result<Entity, BuildError> {
        Ok(Entity {
            field_a: self.field_a,
            field_b: self.field_b,
            field_c: self.field_c,
            flag_a: self.flag_a,
            flag_b: self.flag_b,
            limit: self.limit,
            optional_field: self.optional_field,
        })
    }
}

// Copy constructor - no builder needed
impl Settings {
    fn from_existing(other: &Settings) -> Self {
        Self {
            config: other.config.clone(),
            enabled: other.enabled,
        }
    }
}
```