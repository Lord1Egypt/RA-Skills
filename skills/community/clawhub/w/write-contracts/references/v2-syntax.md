# Move V2 Syntax Patterns

Modern Move V2 syntax features: receiver-style method calls, vector indexing, and lambdas.

## Pattern 1: Receiver-Style Method Calls

Use `self` as first parameter name to enable dot notation.

```move
struct Item has key {
    owner: address,
    value: u64,
}

// ✅ CORRECT: Use 'self' as first parameter
public fun is_owner(self: &Object<Item>, user: &signer): bool acquires Item {
    let item_data = borrow_global<Item>(object::object_address(self));
    item_data.owner == signer::address_of(user)
}

public fun get_value(self: &Object<Item>): u64 acquires Item {
    let item_data = borrow_global<Item>(object::object_address(self));
    item_data.value
}

// ✅ CORRECT: Call with dot notation
public entry fun update_if_owner(
    user: &signer,
    item: Object<Item>,
    new_value: u64
) acquires Item {
    assert!(item.is_owner(user), E_NOT_OWNER);  // Receiver-style call
    // Update logic...
}
```

## Pattern 2: Vector Indexing

Use `vector[index]` syntax instead of `vector::borrow()`.

```move
struct Registry has key {
    items: vector<u64>,
}

// ✅ CORRECT: Use vector[index] syntax
public fun get_item(registry: &Registry, index: u64): u64 {
    *&registry.items[index]  // V2 index notation
}

public fun update_item(registry: &mut Registry, index: u64, value: u64) {
    *&mut registry.items[index] = value;  // V2 mutable index
}

// ✅ CORRECT: Iterate with index notation
public fun sum_all(registry: &Registry): u64 {
    let sum = 0;
    let i = 0;
    let len = vector::length(&registry.items);

    while (i < len) {
        sum = sum + registry.items[i];  // Clean V2 syntax
        i = i + 1;
    };

    sum
}
```

## Pattern 3: Inline Functions with Lambdas

```move
/// Filter items by predicate
inline fun filter_items<T: copy + drop>(
    items: &vector<T>,
    pred: |&T| bool
): vector<T> {
    let result = vector::empty<T>();
    let i = 0;
    while (i < vector::length(items)) {
        let item = vector::borrow(items, i);
        if (pred(item)) {
            vector::push_back(&mut result, *item);
        };
        i = i + 1;
    };
    result
}

/// Get expensive items (price > 1000)
public fun get_expensive_items(
    marketplace: Object<Marketplace>
): vector<Object<Item>> acquires Marketplace {
    let marketplace_data = borrow_global<Marketplace>(
        object::object_address(&marketplace)
    );

    filter_items(&marketplace_data.items, |item| {
        get_item_price(*item) > 1000
    })
}
```

## See Also

- `../../../../patterns/move/MOVE_V2_SYNTAX.md` - Complete V2 syntax guide
