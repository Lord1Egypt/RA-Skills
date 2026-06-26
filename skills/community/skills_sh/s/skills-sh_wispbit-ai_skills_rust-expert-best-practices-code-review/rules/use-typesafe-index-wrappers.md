---
title: Use Type-Safe Index Wrappers
impact: CRITICAL
impactDescription: Prevents index mixing bugs at compile time through newtype pattern
tags: type-safety, newtype, indices, compile-time-safety, rust
---

## Use Type-Safe Index Wrappers

**Impact: CRITICAL (Prevents index mixing bugs at compile time through newtype pattern)**

Use type-safe index wrappers instead of raw primitive types (like `usize`) when working with index-based data structures to prevent mixing different index types.

**Index Wrapper Requirements**

Each index type should be a newtype wrapper with:
- **Derive traits**: `Debug`, `Clone`, `Copy`, `PartialEq`, `Eq`
- **Constructor method**: `new(index: primitive_type) -> Self`
- **Accessor method**: `get(self) -> primitive_type`
- **Hash trait**: Add `Hash` if the index will be used as a key in collections

**Function Parameters**

Functions that accept indices should use the specific index type rather than raw primitives to ensure type safety at compile time.

### BAD Examples

```rust
// src/container.rs
// Raw usize for different index types
pub struct Container {
    items_a: Vec<Foo>,
    items_b: Vec<Bar>,
}

impl Container {
    pub fn get_a(&self, index: usize) -> &Foo {
        &self.items_a[index]
    }

    pub fn get_b(&self, index: usize) -> &Bar {
        &self.items_b[index]
    }
}

// src/processor.rs
// Risk of mixing indices in complex operations
pub struct Processor {
    items_a: Vec<Foo>,
    items_b: Vec<Bar>,
}

impl Processor {
    pub fn link(&mut self, a_idx: usize, b_idx: usize) {
        // Could accidentally mix A and B indices
        self.items_a[b_idx].attach(a_idx);
    }
}
```

### GOOD Examples

```rust
// src/indices.rs
// Type-safe index wrappers
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct IndexA(usize);

impl IndexA {
    pub fn new(index: usize) -> Self {
        Self(index)
    }

    pub fn get(self) -> usize {
        self.0
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct IndexB(usize);

impl IndexB {
    pub fn new(index: usize) -> Self {
        Self(index)
    }

    pub fn get(self) -> usize {
        self.0
    }
}

// src/container.rs
use crate::indices::{IndexA, IndexB};

// Using type-safe indices prevents mixing
pub struct Container {
    items_a: Vec<Foo>,
    items_b: Vec<Bar>,
}

impl Container {
    pub fn get_a(&self, index: IndexA) -> &Foo {
        &self.items_a[index.get()]
    }

    pub fn get_b(&self, index: IndexB) -> &Bar {
        &self.items_b[index.get()]
    }
}
```