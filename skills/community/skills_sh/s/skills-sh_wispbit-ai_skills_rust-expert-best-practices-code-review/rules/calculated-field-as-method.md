---
title: Implement Calculated Fields as Methods
impact: MEDIUM-HIGH
impactDescription: Prevents data duplication and maintains single source of truth
tags: struct-design, methods, calculated-fields, data-modeling, rust
---

## Implement Calculated Fields as Methods

**Impact: MEDIUM-HIGH (Prevents data duplication and maintains single source of truth)**

Calculated fields that are derived from mathematical operations on other struct fields should be implemented as methods rather than stored as separate fields.

**Mathematical Operations**
Target fields assigned using mathematical expressions (`+`, `-`, `*`, `/`, `%`) on other struct fields during construction or initialization.

**Exceptions**
- Fields assigned from method calls or external computations
- Performance-critical code where recalculation is expensive
- Fields representing cached/memoized values with explicit cache invalidation
- Values computed once and never change (immutable computed fields)
- Computations involving external data sources like timestamps, database values, API responses, or data from other objects

### BAD Examples

```rust
// Mathematical computation between struct fields in constructor
impl Foo {
    pub fn new(a: f64, b: f64) -> Self {
        Self {
            a,
            b,
            computed: a * b,  // Should be method
            derived: 2.0 * (a + b),  // Should be method
        }
    }
}

// Percentage calculation in struct initialization
impl Bar {
    pub fn new(count: u32, total: u32) -> Self {
        Self {
            count,
            total,
            rate: (count as f64 / total as f64) * 100.0,  // Should be method
        }
    }
}
```

### GOOD Examples

```rust
// Calculated fields as methods
impl Foo {
    pub fn new(a: f64, b: f64) -> Self {
        Self { a, b }
    }

    pub fn computed(&self) -> f64 {
        self.a * self.b
    }

    pub fn derived(&self) -> f64 {
        2.0 * (self.a + self.b)
    }
}

// External data computation (allowed)
impl Baz {
    pub fn new(base: i64, offset: i64) -> Self {
        Self {
            value: base - offset,  // External computation
            kind: Kind::Default,
        }
    }
}

// Method call assignment (allowed)
impl Qux {
    pub fn new(x: f64, y: f64, processor: &Processor) -> Self {
        Self {
            x,
            y,
            output: processor.compute(x, y),  // Method call
        }
    }
}