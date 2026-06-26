---
title: Use Borrowed Argument Types Instead of Owned Types
impact: HIGH
impactDescription: Improves API flexibility and enables deref coercion for better ergonomics
tags: api-design, function-parameters, deref-coercion, ergonomics, rust
---

## Use Borrowed Argument Types Instead of Owned Types

**Impact: HIGH (Improves API flexibility and enables deref coercion for better ergonomics)**

Use borrowed argument types instead of references to owned types in function parameters.

**Specific Replacements:**

- `&String` → `&str`
- `&Vec<T>` → `&[T]`
- `&PathBuf` → `&Path`
- `&Box<T>` → `&T`

This enables better API flexibility by accepting both owned and borrowed types through Rust's deref coercion.

### BAD Examples

```rust
// src/lib.rs
use std::path::PathBuf;

// &String prevents passing string literals
fn three_vowels(word: &String) -> bool {
    word.chars().filter(|c| "aeiou".contains(*c)).count() >= 3
}

// &Vec<T> prevents passing arrays or slices
fn sum_numbers(nums: &Vec<i32>) -> i32 {
    nums.iter().sum()
}

// &PathBuf prevents passing &Path
fn read_config(path: &PathBuf) -> String {
    std::fs::read_to_string(path).unwrap()
}

// &Box<T> adds unnecessary indirection
struct MyStruct {
    value: i32,
}

fn process_data(data: &Box<MyStruct>) -> i32 {
    data.value * 2
}
```

### GOOD Examples

```rust
// src/lib.rs
use std::path::Path;

// &str accepts both &str and &String
fn three_vowels(word: &str) -> bool {
    word.chars().filter(|c| "aeiou".contains(*c)).count() >= 3
}

// &[T] accepts Vec, arrays, and slices
fn sum_numbers(nums: &[i32]) -> i32 {
    nums.iter().sum()
}

// &Path accepts both PathBuf and &Path
fn read_config(path: &Path) -> String {
    std::fs::read_to_string(path).unwrap()
}

// &T removes unnecessary indirection
struct MyStruct {
    value: i32,
}

fn process_data(data: &MyStruct) -> i32 {
    data.value * 2
}
```