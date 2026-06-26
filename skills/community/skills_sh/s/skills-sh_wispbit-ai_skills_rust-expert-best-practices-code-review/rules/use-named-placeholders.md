---
title: Use Named Placeholders in Destructuring
impact: MEDIUM
impactDescription: Improves code readability and self-documentation
tags: pattern-matching, destructuring, readability, self-documenting, rust
---

## Use Named Placeholders in Destructuring

**Impact: MEDIUM (Improves code readability and self-documentation)**

Use named placeholders instead of bare `_` when destructuring structs in match patterns or let bindings.

When destructuring structs with unused fields, provide descriptive names followed by `_` rather than using bare `_` placeholders. This makes the code more readable and self-documenting by clearly indicating what fields are being ignored.

### BAD Examples

```rust
// Bare underscore placeholders in match
match self {
    Self::Rocket { _, _, .. } => { /* ... */ }
}

// Multiple bare underscores in let binding
let User { _, _, name, .. } = user;

// Function parameters with bare underscore
fn process_data(Data { _, value, .. }: Data) {
    println!("{}", value);
}

// Pattern matching with bare underscores
if let Config { _, enabled, .. } = config {
    return enabled;
}
```

### GOOD Examples

```rust
// Named placeholders showing what's being ignored
match self {
    Self::Rocket { has_fuel: _, has_crew: _, .. } => { /* ... */ }
}

// Clear field names in let binding
let User { id: _, email: _, name, .. } = user;

// Self-documenting function parameters
fn process_data(Data { timestamp: _, value, .. }: Data) {
    println!("{}", value);
}

// Pattern matching with named placeholders
if let Config { debug_mode: _, enabled, .. } = config {
    return enabled;
}
```