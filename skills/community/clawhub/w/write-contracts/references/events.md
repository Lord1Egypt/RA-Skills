# Event Emission Patterns

Patterns for emitting events in Move V2 contracts.

## Basic Event Pattern

```move
use aptos_framework::event;

// Define event with #[event] attribute
#[event]
struct ItemCreated has drop, store {
    item_id: address,
    creator: address,
    name: String,
    timestamp: u64,
}

/// Emit event after creating item
public entry fun create_item(creator: &signer, name: String) {
    let creator_addr = signer::address_of(creator);

    // Create item...
    let constructor_ref = object::create_object(creator_addr);
    let item_addr = object::address_from_constructor_ref(&constructor_ref);

    // Emit event
    event::emit(ItemCreated {
        item_id: item_addr,
        creator: creator_addr,
        name,
        timestamp: aptos_framework::timestamp::now_seconds(),
    });
}
```

## Event Best Practices

1. **Define with #[event] attribute** and `has drop, store` abilities
2. **Emit AFTER state changes** (not before)
3. **Include relevant context**: WHO, WHAT, WHEN
4. **Use past tense names**: `ItemCreated`, `ListingCancelled`, `TokenTransferred`
5. **Design for indexing**: Include addresses and IDs for easy querying

## See Also

- `complete-example.md` - Full contract with events
