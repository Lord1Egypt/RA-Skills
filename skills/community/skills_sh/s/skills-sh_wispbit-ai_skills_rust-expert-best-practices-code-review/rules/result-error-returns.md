---
title: Proper Error Handling in Result-Returning Functions
impact: CRITICAL
impactDescription: Ensures proper error propagation and prevents panics in error paths
tags: error-handling, result, question-mark-operator, unwrap, rust
---

## Proper Error Handling in Result-Returning Functions

**Impact: CRITICAL (Ensures proper error propagation and prevents panics in error paths)**

Functions that return `Result` types must use proper error handling patterns and avoid redundant error handling constructs.

**Avoid `.unwrap()` and `.expect()`**
Use the `?` operator instead of `.unwrap()` or `.expect()` methods to properly propagate errors. Exception: `.await.expect("message")?` is acceptable for handling task join results where you expect the task to succeed but want to propagate the inner Result.

**Avoid Redundant Error Handling Patterns**
- Don't use `if let Err(e)` pattern followed by `return Err(e)` when you can use `?` operator
- Don't use `.map_err(|e| e)?` to forward errors unchanged
- Don't use `.and_then(|v| Ok(v))?` for identity transformations
- For async code, avoid `.await.unwrap()?` pattern which defeats error propagation

### BAD Examples

```rust
// src/handlers/user.rs
use std::error::Error;

// Using unwrap() in Result-returning function
fn read_number() -> Result<i32, std::num::ParseIntError> {
    let s = "123";
    let n: i32 = s.parse::<i32>().unwrap(); // BAD: panic on invalid input
    Ok(n)
}

// Using expect() in Result-returning function
fn process_data() -> Result<String, Box<dyn Error>> {
    let data = fetch_data().expect("Failed to fetch data");
    Ok(data.to_string())
}

// Redundant if let Err pattern
fn handle_result() -> Result<i32, MyError> {
    if let Err(e) = some_operation() {
        return Err(e);
    }
    let value = some_operation().unwrap();
    Ok(value)
}

// Redundant map_err forwarding
fn forward_error() -> Result<String, MyError> {
    let value = some_result.map_err(|e| e)?;
    Ok(value)
}

// Async unwrap defeating error propagation
async fn async_handler() -> Result<Value, MyError> {
    let value = handle.await.unwrap()?; // BAD: panics on task failure
    Ok(value)
}
```

### GOOD Examples

```rust
// src/handlers/user.rs
use std::error::Error;

// Using ? operator for error propagation
fn read_number() -> Result<i32, std::num::ParseIntError> {
    let s = "123";
    let n: i32 = s.parse()?; // GOOD: returns Err on failure
    Ok(n)
}

// Using ? operator with different error types
fn process_data() -> Result<String, Box<dyn Error>> {
    let data = fetch_data()?;
    Ok(data.to_string())
}

// Direct use of ? operator
fn handle_result() -> Result<i32, MyError> {
    let value = some_operation()?;
    Ok(value)
}

// Direct error propagation
fn forward_error() -> Result<String, MyError> {
    let value = some_result?;
    Ok(value)
}

// Proper async error handling
async fn async_handler() -> Result<Value, MyError> {
    let value = handle.await?; // GOOD: handles async errors properly
    Ok(value)
}

// Acceptable: await.expect()?
async fn handle_task_join() -> Result<Value, MyError> {
    let writer = task_handle.await.expect("Expected task to succeed")?;
    Ok(writer)
}

// Functions not returning Result can use unwrap (not covered by this rule)
fn main() {
    let n = "123".parse::<i32>().unwrap(); // OK: main doesn't return Result
    println!("{}", n);
}
```