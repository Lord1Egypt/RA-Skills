---
title: Avoid Boolean Parameters in Function Signatures
impact: MEDIUM-HIGH
impactDescription: Improves code readability and prevents boolean confusion at call sites
tags: api-design, function-parameters, enums, readability, rust
---

## Avoid Boolean Parameters in Function Signatures

**Impact: MEDIUM-HIGH (Improves code readability and prevents boolean confusion at call sites)**

Avoid boolean parameters in function signatures. Boolean parameters make code hard to read at the call site and are error-prone.

Replace boolean parameters with enums or parameter structs for better readability and type safety.

### BAD Examples

```rust
// src/data_processor.rs
// Multiple boolean parameters are unclear at call site
fn process_data(data: &[u8], compress: bool, encrypt: bool, validate: bool) {
    // Implementation details
}

// What do these booleans mean?
process_data(&data, true, false, true);

// src/email_service.rs
// Even single booleans can be unclear
fn send_email(recipient: &str, urgent: bool) {
    // Implementation
}

send_email("user@example.com", true);  // What does true mean?

// src/database.rs
// Constructor with boolean flags
impl DatabaseConnection {
    fn new(host: &str, use_ssl: bool, auto_reconnect: bool) -> Self {
        // Implementation
    }
}
```

### GOOD Examples

```rust
// src/good_processor.rs
// Use enums for boolean-like choices
enum Compression {
    Enabled,
    Disabled,
}

enum Encryption {
    Enabled,
    Disabled,
}

fn process_data(data: &[u8], compression: Compression, encryption: Encryption) {
    // Implementation
}

// Self-documenting call site
process_data(&data, Compression::Enabled, Encryption::Disabled);

// src/good_options.rs
// For many options, use parameter structs
struct ProcessOptions {
    compression: bool,
    encryption: bool,
    validation: bool,
}

fn process_with_options(data: &[u8], options: ProcessOptions) {
    // Implementation
}

process_with_options(&data, ProcessOptions {
    compression: true,
    encryption: false,
    validation: true,
});

// src/good_builder.rs
// Builder pattern for complex configurations
impl DatabaseConnection {
    fn builder() -> DatabaseConnectionBuilder {
        DatabaseConnectionBuilder::new()
    }
}

struct DatabaseConnectionBuilder {
    host: String,
    use_ssl: bool,
    auto_reconnect: bool,
}

impl DatabaseConnectionBuilder {
    fn with_ssl(mut self) -> Self {
        self.use_ssl = true;
        self
    }

    fn with_auto_reconnect(mut self) -> Self {
        self.auto_reconnect = true;
        self
    }
}
```