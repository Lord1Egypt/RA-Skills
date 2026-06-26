# Access Control Patterns

Role-based access control (RBAC) and permission patterns for Move contracts.

## Pattern: Role-Based Access Control

```move
struct Marketplace has key {
    admin: address,
    operators: vector<address>,
    paused: bool,
}

const E_NOT_ADMIN: u64 = 1;
const E_NOT_OPERATOR: u64 = 2;

/// Admin-only function
public entry fun add_operator(
    admin: &signer,
    operator_addr: address
) acquires Marketplace {
    let marketplace = borrow_global_mut<Marketplace>(@my_addr);
    assert!(signer::address_of(admin) == marketplace.admin, E_NOT_ADMIN);

    vector::push_back(&mut marketplace.operators, operator_addr);
}

/// Operator-only function
public entry fun pause(operator: &signer) acquires Marketplace {
    let marketplace = borrow_global_mut<Marketplace>(@my_addr);
    let operator_addr = signer::address_of(operator);

    assert!(
        vector::contains(&marketplace.operators, &operator_addr),
        E_NOT_OPERATOR
    );

    marketplace.paused = true;
}
```

## Best Practices

1. **Verify permissions before modifying state**
2. **Use hierarchical roles** (Owner > Admin > Moderator)
3. **Emit events** when roles are granted/revoked
4. **Implement pause functionality** for emergency controls

## See Also

- `object-patterns.md` - Object ownership patterns
- `../../../../patterns/move/SECURITY.md` - Complete security checklist
