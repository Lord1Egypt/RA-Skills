---
title: Use .copied() for Copy Types in Iterators
impact: MEDIUM
impactDescription: Simplifies dereferencing patterns and improves code readability
tags: iterators, copy-types, dereferencing, readability, rust
---

## Use .copied() for Copy Types in Iterators

**Impact: MEDIUM (Simplifies dereferencing patterns and improves code readability)**

When iterating over collections containing Copy types (like `usize`, `i32`, `bool`, etc.), use `.copied()` to avoid complex dereferencing patterns with multiple reference layers.

**Apply when:**
- Iterating over collections containing Copy types
- The iterator closure uses multiple dereference patterns (`&&&`, `&&`, etc.)
- The type being dereferenced implements the Copy trait

### BAD Examples

```rust
// src/lib.rs
fn filter_numbers(input: &[usize]) -> Vec<usize> {
    input
        .iter()
        .filter(|&&&x| x > 5)
        .collect()
}

// src/lib.rs
fn filter_bools(input: &[bool]) -> Vec<bool> {
    input
        .iter()
        .filter(|&&x| x)
        .collect()
}

// src/processing.rs
fn process_integers(input: &[i32]) -> Vec<i32> {
    input
        .iter()
        .map(|&&&x| x * 2)
        .filter(|&&&y| y > 10)
        .collect()
}

// src/math.rs
fn double_values(input: &[f64]) -> Vec<f64> {
    input
        .iter()
        .map(|&&x| x * 2.0)
        .collect()
}
```

### GOOD Examples

```rust
// src/lib.rs
fn filter_numbers(input: &[usize]) -> Vec<usize> {
    input
        .iter()
        .copied()
        .filter(|&x| x > 5)
        .collect()
}

// src/lib.rs
fn filter_bools(input: &[bool]) -> Vec<bool> {
    input
        .iter()
        .copied()
        .filter(|x| *x)
        .collect()
}

// src/strings.rs
fn filter_strings(input: &[String]) -> Vec<&String> {
    input
        .iter()
        .filter(|&s| s.len() > 5)
        .collect()
}

// src/sum.rs
fn sum_positive(input: &[i32]) -> i32 {
    input
        .iter()
        .filter(|&x| *x > 0)
        .sum()
}
```