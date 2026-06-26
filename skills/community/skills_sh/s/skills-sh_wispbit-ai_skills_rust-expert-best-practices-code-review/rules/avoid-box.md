---
title: Avoid Unnecessary Box<T> for Concrete Types
impact: MEDIUM
impactDescription: Reduces unnecessary heap allocations and improves performance
tags: box, heap-allocation, performance, memory-management, rust
---

## Avoid Unnecessary Box<T> for Concrete Types

**Impact: MEDIUM (Reduces unnecessary heap allocations and improves performance)**

Do not use `Box<T>` wrapper for concrete types unless there is a legitimate reason for heap allocation. `Box<T>` should only be used in specific scenarios where it provides necessary functionality, not as a default choice.

**Valid reasons to use `Box<T>` with concrete types:**
- **Complex generic types** like `GenericWriter<ChunkedWriter>` where the compiler cannot determine size at compile time
- **Recursive types** or deeply nested generics that would cause stack overflow
- **Types where the exact size varies** based on runtime conditions
- **Enum variants** to prevent the enum from becoming too large

**Note:** This rule only applies to concrete type identifiers. `Box<dyn Trait>` for trait objects is always acceptable and not checked by this rule.

### BAD Examples

```rust
// src/simple.rs
type Result<T> = std::result::Result<T, String>;

pub fn get_number() -> Result<Box<i32>> {
    Ok(Box::new(42))
}

// src/data.rs
struct Record {
    id: u32,
    name: String,
}

pub fn create_record(name: String) -> Box<Record> {
    Box::new(Record { id: 1, name })
}

// src/collections.rs
use std::collections::HashMap;

pub fn get_config() -> Box<HashMap<String, String>> {
    Box::new(HashMap::new())
}
```

### GOOD Examples

```rust
// src/adapter.rs
use std::fmt::Debug;

trait Processor<Input, Output> {
    fn process(&self, input: Input) -> Output;
}

#[derive(Debug)]
pub struct ProcessorAdapter<Input, Output> {
    // Box<dyn Trait> is acceptable for trait objects
    processor: Box<dyn Processor<Input, Output>>,
}

// src/recursive.rs
// Recursive type requires Box for heap allocation
pub enum Node {
    Leaf(i32),
    Branch(Box<Node>, Box<Node>),
}

// src/complex.rs
use std::io::Write;

// Complex generic type where size is unknown at compile time
pub struct Writer<W: Write> {
    inner: Box<GenericWriter<ChunkedWriter<W>>>,
}
```