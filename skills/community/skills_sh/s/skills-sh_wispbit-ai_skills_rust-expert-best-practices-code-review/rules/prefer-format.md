---
title: Prefer format! Over Manual String Concatenation
impact: MEDIUM
impactDescription: Improves code clarity and reduces string building complexity
tags: strings, format-macro, concatenation, readability, rust
---

## Prefer format! Over Manual String Concatenation

**Impact: MEDIUM (Improves code clarity and reduces string building complexity)**

Prefer `format!` over manual string concatenation when building strings from multiple pieces (literals + variables).

**Manual String Building**
Avoid using `push_str`, `push`, or `+` operator on a fresh `String` when a single `format!` call would be clearer.

**Performance Note**
This rule prioritizes code clarity over micro-optimizations. Use `format!` unless performance profiling shows string building is a bottleneck.

### BAD Examples

```rust
// Multiple push operations
let mut s = "Hello ".to_owned();
s.push_str(name);
s.push('!');

// String concatenation with +
let message = "Error: ".to_string() + &error_code + " - " + &description;

// Mixed push operations
let mut path = base_dir.to_string();
path.push('/');
path.push_str(&filename);
path.push_str(".txt");
```

### GOOD Examples

```rust
// Single format! call
let s = format!("Hello {name}!");

// Format with multiple variables
let message = format!("Error: {error_code} - {description}");

// Format for path building
let path = format!("{base_dir}/{filename}.txt");

// Simple single operation (acceptable)
let mut s = base.to_string();
s.push_str(suffix);
```