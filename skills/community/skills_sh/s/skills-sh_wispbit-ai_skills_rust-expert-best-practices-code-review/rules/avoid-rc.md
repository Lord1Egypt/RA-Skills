---
title: Avoid Unnecessary Rc<T> Usage
impact: MEDIUM
impactDescription: Simplifies ownership patterns and reduces reference counting overhead
tags: ownership, rc, memory-management, performance, rust
---

## Avoid Unnecessary Rc<T> Usage

**Impact: MEDIUM (Simplifies ownership patterns and reduces reference counting overhead)**

Avoid unnecessary use of `Rc<T>` when simpler ownership patterns would suffice.

**Function Parameters**

Use borrowed references (`&T` or `&[T]`) instead of `Rc<T>` for function parameters that only need to read data, unless the parameter type is part of a system architecture that intentionally uses `Rc` for shared ownership.

**Struct Fields**

Don't wrap struct fields in `Rc<T>` unless multiple owners genuinely need to share the same data instance.

**Valid Use Cases for Rc<T>**

- Multiple components need to share the same immutable data instance (shared configuration, metadata, reference data)
- System architecture intentionally uses `Rc` for shared ownership throughout the codebase (e.g., trait methods that require `Rc<T>` parameters for event processing)

### BAD Examples

```rust
// src/module.rs
use std::rc::Rc;

// Function parameter wrapped in Rc unnecessarily
fn compute_total(items: Rc<Vec<i32>>) -> i32 {
    items.iter().sum()
}

// src/models/mod.rs
use std::rc::Rc;

// Struct fields wrapped in Rc without sharing need
struct Data {
    label: Rc<String>,
    items: Rc<Vec<i32>>,
}

// Using Rc just to avoid ownership thinking
fn build_data() -> Data {
    Data {
        label: Rc::new("x".to_string()),
        items: Rc::new(vec![1, 2, 3]),
    }
}
```

### GOOD Examples

```rust
// src/module.rs
// Simple borrowed reference for read-only access
fn compute_total(items: &[i32]) -> i32 {
    items.iter().sum()
}

// src/models/mod.rs
// Owned data in struct when no sharing needed
struct Data {
    label: String,
    items: Vec<i32>,
}

// src/services/mod.rs
use std::rc::Rc;

struct Config {
    value: String,
}

struct Handler {
    config: Rc<Config>, // Multiple handlers share same config
}

// Rc used for legitimate shared ownership
fn build_handlers() -> (Handler, Handler) {
    let config = Rc::new(Config { value: "x".into() });
    (
        Handler { config: config.clone() },
        Handler { config: config.clone() },
    )
}

// src/core/mod.rs
use std::rc::Rc;

// System architecture using Rc for shared event data
trait HandlerTrait {
    type In: Event;
    fn process(&self, input: Rc<Self::In>, ctx: &dyn Context) -> Vec<Box<dyn Event>>;
}

trait Event {}
trait Context {}

struct EventData;
impl Event for EventData {}

struct ProcessedData {
    source: Rc<EventData>, // Shared reference as part of architecture
}
impl Event for ProcessedData {}
```