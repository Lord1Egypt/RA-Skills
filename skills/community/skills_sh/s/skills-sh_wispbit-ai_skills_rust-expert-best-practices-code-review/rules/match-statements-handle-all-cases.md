---
title: Match Statements Should Handle All Cases Explicitly
impact: HIGH
impactDescription: Prevents bugs when new enum variants are added through exhaustive matching
tags: pattern-matching, enums, exhaustive-match, type-safety, rust
---

## Match Statements Should Handle All Cases Explicitly

**Impact: HIGH (Prevents bugs when new enum variants are added through exhaustive matching)**

Match statements should explicitly handle all enum variants instead of using catch-all patterns (`_` or `..`).

Catch-all patterns can hide bugs when new enum variants are added, as the compiler won't warn about unhandled cases. Instead, explicitly list all variants or group related variants using the `|` operator.

### BAD Examples

```rust
// Example enum (defined elsewhere, e.g. crate::types)
enum State {
    A,
    B,
    C,
    D,
}

// Using catch-all pattern
fn process_state(state: State) -> String {
    match state {
        State::A => "processing a".to_string(),
        State::B => "processing b".to_string(),
        _ => "default handling".to_string(), // Hides unhandled variants
    }
}

// Using wildcard catch-all
fn handle_value(value: i32) -> String {
    match value {
        1 => "one".to_string(),
        2 => "two".to_string(),
        _ => "rest".to_string(), // Catch-all for remaining values
    }
}

// Example enum (defined elsewhere)
enum Kind {
    X,
    Y,
    Z,
}

// Multiple catch-all patterns
fn route(kind: Kind, level: i32) -> String {
    match (kind, level) {
        (Kind::X, 1) => "high priority".to_string(),
        (Kind::Y, _) => "standard".to_string(),
        _ => "fallback".to_string(), // Catch-all tuple pattern
    }
}
```

### GOOD Examples

```rust
// Example enum (defined elsewhere, e.g. crate::types)
enum State {
    A,
    B,
    C,
    D,
}

// Explicitly handle all variants
fn process_state(state: State) -> String {
    match state {
        State::A => "processing a".to_string(),
        State::B => "processing b".to_string(),
        State::C => "processing c".to_string(),
        State::D => "processing d".to_string(),
    }
}

// Example enum (defined elsewhere)
enum Kind {
    X,
    Y,
    Z,
    W,
}

// Group related variants
fn route(kind: Kind) -> String {
    match kind {
        Kind::X | Kind::Y => "high priority".to_string(),
        Kind::Z | Kind::W => "standard priority".to_string(),
    }
}

// std::result::Result — explicit handling with all possible outcomes
fn handle_result(result: Result<i32, String>) -> String {
    match result {
        Ok(value) => format!("success: {}", value),
        Err(error) => format!("error: {}", error),
    }
}
```