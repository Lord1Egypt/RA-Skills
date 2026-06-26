---
title: Avoid Panic - Use Appropriate Error Handling
impact: CRITICAL
impactDescription: Prevents unexpected crashes and enables graceful error handling
tags: error-handling, panic, assert, result, rust
---

## Avoid Panic - Use Appropriate Error Handling

**Impact: CRITICAL (Prevents unexpected crashes and enables graceful error handling)**

Use appropriate error handling methods instead of `panic!` based on the context and function signature.

**Invariant Validation**
Use `assert!` for validation that checks program invariants and state consistency:
- Input parameter validation
- Business logic constraints
- Data integrity checks
- State validation and consistency checks

**Functions Returning Result**
In functions that return `Result`, use proper error handling instead of `panic!`:
- Use `map_err` to convert errors into the expected error type
- Return errors using the `?` operator or explicit `Err()` returns
- Avoid `panic!`, `unwrap()`, or `unwrap_or_else(|| panic!(...))` patterns

**Functions Not Returning Result**
Functions that use `panic!` for error handling should consider returning `Result` instead:
- Replace `panic!` with proper error types and `Err()` returns
- Update the function signature to return `Result<T, ErrorType>`
- This allows callers to handle errors gracefully rather than crashing

**Unrecoverable Program States**
Reserve `panic!` for situations where the program is in an invalid and unrecoverable state:
- Critical system initialization failures (including main function startup validation)
- Unreachable code paths in match statements
- Critical system component failures that cannot be recovered from

**Debug-Only Validation**
Use `debug_assert!` for validation that should only run in debug builds:
- Internal consistency checks
- Performance-sensitive validation
- Developer-focused assertions

**Error Messages with expect**
When using `unwrap()` followed by `panic!` with an error message, or `unwrap_or_else(|| panic!(...))` patterns, use `expect` instead:
- Replace `unwrap_or_else(|| panic!("message"))` with `expect("message")`
- Replace manual unwrap + panic patterns with chained `expect` calls

### BAD Examples

```rust
// src/validation.rs
// Input validation should use assert!
fn validate_items(items: &[Record]) {
    if items.is_empty() {
        panic!("collection must contain at least one item");
    }
}

// Business logic validation should use assert!
fn validate_constraint(c: &Constraint) {
    if c.max <= 0 {
        panic!("max must be positive");
    }
}

// src/calculator.rs
// Function should return Result instead of panicking
fn compute_ratio_bad(num: u32, denom: u32) -> f32 {
    if denom == 0 {
        panic!("denominator cannot be zero");
    }

    if num > denom {
        panic!("numerator exceeds denominator");
    }

    (num as f32 / denom as f32) * 100.0
}

// src/parser.rs
// Result functions should use proper error handling
pub fn parse_int(value: &str, line: usize) -> Result<i64, std::io::Error> {
    let parsed = value.parse::<i64>().unwrap_or_else(|err| {
        panic!(
            "Failed to parse '{}' as i64 at line {}: {}",
            value,
            line + 1,
            err
        )
    });

    if parsed < 0 {
        panic!("Value must be non-negative: {} at line {}", parsed, line + 1);
    }

    Ok(parsed)
}

// src/data.rs
// Use expect instead of unwrap + panic pattern
fn get_field_typed<T>(tbl: &DataTable, col: &str) -> &T {
    if let Some(arr) = tbl.column(col) {
        arr.as_any().downcast_ref::<T>().unwrap()
    } else {
        panic!("Missing column '{col}' in table");
    }
}
```

### GOOD Examples

```rust
// src/validation.rs
// Input validation with assert!
fn validate_items(items: &[Record]) {
    assert!(!items.is_empty(), "collection must contain at least one item");
}

// Business logic validation with assert!
fn validate_constraint(c: &Constraint) {
    assert!(c.max > 0, "max must be positive");
}

// src/calculator.rs
enum RatioError {
    ZeroDenom,
    OutOfRange { num: u32, denom: u32 },
}

// Function returning Result instead of panicking
fn compute_ratio(num: u32, denom: u32) -> Result<f32, RatioError> {
    if denom == 0 {
        return Err(RatioError::ZeroDenom);
    }

    if num > denom {
        return Err(RatioError::OutOfRange { num, denom });
    }

    Ok((num as f32 / denom as f32) * 100.0)
}

// src/app.rs
// Critical initialization failures (acceptable panic!)
async fn run(cfg: Config) -> Result<Output, AppError> {
    if cfg.inputs.is_empty() {
        panic!("No inputs configured");
    }
    // Continue processing...
}

// src/evaluator.rs
// Unreachable code paths (acceptable panic!)
fn eval_expr(expr: &Expr) -> Value {
    match expr {
        Expr::Int(n) => Value::Int(*n),
        Expr::Str(s) => Value::Str(s.clone()),
        _ => panic!("unreachable: invalid expr kind"),
    }
}

// src/parser.rs
// Proper error handling in Result functions
pub fn parse_int(value: &str, line: usize) -> Result<i64, std::io::Error> {
    let parsed = value.parse::<i64>().map_err(|err| {
        std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            format!("Failed to parse '{}' as i64 at line {}: {}", value, line + 1, err),
        )
    })?;

    if parsed < 0 {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidData,
            format!("Value must be non-negative: {} at line {}", parsed, line + 1),
        ));
    }

    Ok(parsed)
}

// src/data.rs
// Use expect instead of unwrap + panic
fn get_field_typed<T>(tbl: &DataTable, col: &str) -> &T {
    tbl.column(col)
        .expect(&format!("Missing column '{col}' in table"))
        .as_any()
        .downcast_ref::<T>()
        .expect(&format!("Column '{col}' is not the expected type"))
}
```