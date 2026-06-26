---
title: Use Exhaustive Enum Deserialization with Pattern Matching
impact: CRITICAL
impactDescription: Prevents invalid states and unsafe vector access through type-level safety
tags: deserialization, type-safety, pattern-matching, serde, enums, rust
---

## Use Exhaustive Enum Deserialization with Pattern Matching

**Impact: CRITICAL (Prevents invalid states and unsafe vector access through type-level safety)**

Use exhaustive enum deserialization with slice pattern matching for safe Vec access in Rust.

**Exhaustive Match Statements**

During deserialization, use explicit match statements on tuples of related fields to handle every meaningful combination. Any invalid combination must produce a descriptive error.

**Vector Slice Pattern Matching**

Use `match vec.as_slice()` with slice patterns (`[]`, `[one]`, `[first, ..]`) instead of `is_empty()` checks followed by indexing.

**Custom Deserializers**

Use `#[serde(deserialize_with = "...")]` to enforce business rules at deserialization boundaries with type-level safety.

**Clear Error Messages**

Errors must specify which fields are present/absent, why the combination is invalid, and what combinations are valid.

### BAD Examples

```rust
// src/models/item.rs
use serde::Deserialize;

// Missing exhaustive matching - allows invalid states
#[derive(Deserialize)]
struct Item {
    field_a: Option<String>,
    field_b: Option<String>,
    flag: bool,
}

impl Item {
    fn validate(&self) -> Result<(), String> {
        // Generic error without context
        if self.field_a.is_some() != self.field_b.is_some() {
            return Err("Invalid state".to_string());
        }
        Ok(())
    }
}

// src/services/element.rs
// Unsafe vector access after is_empty check
fn get_first_element<T>(elements: Vec<T>) -> Option<T> {
    if !elements.is_empty() {
        Some(elements[0].clone()) // Unsafe indexing
    } else {
        None
    }
}
```

### GOOD Examples

```rust
// src/models/config.rs
use serde::{Deserialize, Deserializer};

#[derive(Deserialize)]
struct ConfigHelper {
    field_a: Option<String>,
    field_b: Option<String>,
    flag: bool,
}

// Custom deserializer with explicit matching + type-level safety
#[derive(Deserialize)]
#[serde(deserialize_with = "deserialize_config")]
enum Config {
    Active { a: String, b: String },
    Inactive,
}

fn deserialize_config<'de, D>(deserializer: D) -> Result<Config, D::Error>
where
    D: Deserializer<'de>,
{
    let helper = ConfigHelper::deserialize(deserializer)?;

    match (helper.field_a, helper.field_b, helper.flag) {
        (Some(a), Some(b), true) => Ok(Config::Active { a, b }),
        (None, None, false) => Ok(Config::Inactive),

        (field_a, field_b, flag) => Err(serde::de::Error::custom(format!(
            "Invalid config combination: field_a_present={}, field_b_present={}, flag={}. \
             Expected either (field_a & field_b present AND flag=true) or (field_a & field_b absent AND flag=false).",
            field_a.is_some(),
            field_b.is_some(),
            flag
        ))),
    }
}

// src/services/element.rs
#[derive(Debug)]
enum ElementError {
    NotFound,
    MultipleMatches,
}

// Safe vector pattern matching (forces handling all cases)
fn pick_single_element<T: Clone>(elements: Vec<T>) -> Result<T, ElementError> {
    match elements.as_slice() {
        [] => Err(ElementError::NotFound),
        [only] => Ok(only.clone()),
        _ => Err(ElementError::MultipleMatches),
    }
}
```