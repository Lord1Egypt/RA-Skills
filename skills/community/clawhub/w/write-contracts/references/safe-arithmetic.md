# Safe Arithmetic Patterns

Patterns for preventing overflow, underflow, and other arithmetic vulnerabilities.

## Overflow Prevention

```move
// Error constants
const E_ZERO_AMOUNT: u64 = 1;
const E_OVERFLOW: u64 = 10;
const MAX_U64: u64 = 18446744073709551615;

/// Safe deposit - check overflow before adding
public entry fun deposit(user: &signer, amount: u64) acquires Account {
    assert!(amount > 0, E_ZERO_AMOUNT);

    let account = borrow_global_mut<Account>(signer::address_of(user));

    // Check overflow before adding
    assert!(account.balance <= MAX_U64 - amount, E_OVERFLOW);

    account.balance = account.balance + amount;
}
```

**Pattern:**

```move
// Before: a + b
// After:
assert!(a <= MAX_U64 - b, E_OVERFLOW);
let result = a + b;
```

## Underflow Prevention

```move
// Error constants
const E_ZERO_AMOUNT: u64 = 1;
const E_UNDERFLOW: u64 = 11;
const E_INSUFFICIENT_BALANCE: u64 = 12;

/// Safe withdrawal - check underflow before subtracting
public entry fun withdraw(user: &signer, amount: u64) acquires Account {
    assert!(amount > 0, E_ZERO_AMOUNT);

    let account = borrow_global_mut<Account>(signer::address_of(user));

    // Check underflow before subtracting
    assert!(account.balance >= amount, E_INSUFFICIENT_BALANCE);

    account.balance = account.balance - amount;
}
```

**Pattern:**

```move
// Before: a - b
// After:
assert!(a >= b, E_UNDERFLOW);
let result = a - b;
```

## Division by Zero Prevention

```move
const E_DIVISION_BY_ZERO: u64 = 13;

/// Safe division
public fun safe_div(numerator: u64, denominator: u64): u64 {
    assert!(denominator > 0, E_DIVISION_BY_ZERO);
    numerator / denominator
}
```

## Percentage Calculations

```move
// Error constants
const E_INVALID_PERCENTAGE: u64 = 14;
const BASIS_POINTS_DIVISOR: u64 = 10000; // 100% = 10000 basis points

/// Calculate percentage of amount
/// percentage: 250 = 2.5%, 1000 = 10%, 10000 = 100%
public fun percentage_of(amount: u64, percentage_bp: u64): u64 {
    assert!(percentage_bp <= BASIS_POINTS_DIVISOR, E_INVALID_PERCENTAGE);

    // Multiply first for precision, then divide
    (amount * percentage_bp) / BASIS_POINTS_DIVISOR
}
```

## Best Practices

1. **Always validate before arithmetic** - Check overflow before addition, underflow before subtraction
2. **Use descriptive error codes** - E_OVERFLOW, E_UNDERFLOW, E_DIVISION_BY_ZERO
3. **Consider precision** - Multiply before dividing, use basis points for percentages
4. **Test edge cases** - Test with MAX_U64, 0, and boundary values

## See Also

- `../../../../patterns/move/SECURITY.md` - Complete security checklist
