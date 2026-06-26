# Object Patterns

Detailed patterns for creating and managing Aptos Move objects.

## Pattern 1: Named Objects (Singletons)

Named objects are deterministic singleton objects created with a unique seed. Perfect for registries, configs, and
global state.

```move
/// Create singleton registry
public fun create_registry(admin: &signer): Object<Registry> {
    let constructor_ref = object::create_named_object(
        admin,
        b"REGISTRY_V1"  // Unique seed
    );

    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, Registry {
        admin: signer::address_of(admin),
        items: vector::empty(),
    });

    object::object_from_constructor_ref<Registry>(&constructor_ref)
}

/// Retrieve registry by reconstructing address
public fun get_registry(creator_addr: address): Object<Registry> {
    let registry_addr = object::create_object_address(&creator_addr, b"REGISTRY_V1");
    object::address_to_object<Registry>(registry_addr)
}
```

**Key points:**

- Use `object::create_named_object()` with a unique seed
- Seed must be unique per creator address
- Can retrieve object deterministically with `object::create_object_address()`
- Perfect for global singletons (registries, configs, admin settings)

## Pattern 2: Collections (Objects Owning Objects)

Objects can own other objects by setting the parent object as the creator.

```move
// Error constants
const E_NOT_OWNER: u64 = 1;

struct Collection has key {
    name: String,
    items: vector<Object<Item>>,
}

struct Item has key {
    name: String,
    parent: Object<Collection>,
}

/// Add item to collection
public entry fun add_item_to_collection(
    owner: &signer,
    collection: Object<Collection>,
    item_name: String
) acquires Collection {
    // Verify ownership
    assert!(object::owner(collection) == signer::address_of(owner), E_NOT_OWNER);

    // Create item owned by collection
    let collection_addr = object::object_address(&collection);
    let constructor_ref = object::create_object(collection_addr);

    let item_obj = object::object_from_constructor_ref<Item>(&constructor_ref);
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, Item {
        name: item_name,
        parent: collection,
    });

    // Add to collection
    let collection_data = borrow_global_mut<Collection>(collection_addr);
    vector::push_back(&mut collection_data.items, item_obj);
}
```

**Key points:**

- Pass collection's address as creator when creating child objects
- Store parent reference in child for bidirectional navigation
- Store child references in parent's vector
- When collection is deleted, all child objects can be deleted too

## Pattern 3: Object Transfer

Use stored TransferRef to enable transfers.

```move
// Error constants
const E_NOT_OWNER: u64 = 1;
const E_ZERO_ADDRESS: u64 = 2;

struct MyObject has key {
    name: String,
    transfer_ref: object::TransferRef,
}

/// Transfer with ownership check
public entry fun transfer_object(
    owner: &signer,
    obj: Object<MyObject>,
    recipient: address
) acquires MyObject {
    // Verify ownership
    assert!(object::owner(obj) == signer::address_of(owner), E_NOT_OWNER);

    // Validate recipient
    assert!(recipient != @0x0, E_ZERO_ADDRESS);

    // Transfer using stored ref
    let obj_data = borrow_global<MyObject>(object::object_address(&obj));
    object::transfer_with_ref(
        object::generate_linear_transfer_ref(&obj_data.transfer_ref),
        recipient
    );
}
```

**Key points:**

- Store `TransferRef` in struct
- Generate `LinearTransferRef` when transferring
- Always verify ownership before transferring
- Validate recipient address (not @0x0)

## Pattern 4: Object Deletion

Use stored DeleteRef to enable deletion.

```move
// Error constants
const E_NOT_OWNER: u64 = 1;

/// Delete with ownership check
public entry fun burn_object(owner: &signer, obj: Object<MyObject>) acquires MyObject {
    // Verify ownership
    assert!(object::owner(obj) == signer::address_of(owner), E_NOT_OWNER);

    // Extract data and delete
    let obj_addr = object::object_address(&obj);
    let MyObject {
        name: _,
        transfer_ref: _,
        delete_ref,
    } = move_from<MyObject>(obj_addr);

    object::delete(delete_ref);
}
```

**Key points:**

- Store `DeleteRef` in struct
- Use `move_from` to extract struct before deleting
- Destructure to access delete_ref
- Always verify ownership before deleting
- Object cannot be deleted if it has children

## Pattern 5: ExtendRef for Object Signer

ExtendRef allows you to get the object's signer after construction.

```move
// Error constants
const E_NOT_OWNER: u64 = 1;

struct MyObject has key {
    name: String,
    extend_ref: object::ExtendRef,
}

public fun create_with_extend_ref(creator: &signer): Object<MyObject> {
    let constructor_ref = object::create_object(signer::address_of(creator));
    let extend_ref = object::generate_extend_ref(&constructor_ref);
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, MyObject {
        name: string::utf8(b"Example"),
        extend_ref,
    });

    object::object_from_constructor_ref<MyObject>(&constructor_ref)
}

/// Update object using extend_ref to get object signer
/// Note: This function allows anyone to update. In production, add authorization checks.
public entry fun update_with_extend_ref(
    owner: &signer,
    obj: Object<MyObject>,
    new_name: String
) acquires MyObject {
    // ✅ IMPORTANT: Verify owner authorization
    assert!(object::owner(obj) == signer::address_of(owner), E_NOT_OWNER);

    let obj_data = borrow_global_mut<MyObject>(object::object_address(&obj));

    // Get object signer from extend_ref
    let object_signer = object::generate_signer_for_extending(&obj_data.extend_ref);

    obj_data.name = new_name;
}
```

**Key points:**

- ExtendRef allows getting object signer after construction
- Useful when object needs to perform actions as itself
- Store ExtendRef in struct during construction
- Use `generate_signer_for_extending()` to get signer later

## See Also

- `../../../../patterns/move/OBJECTS.md` - Comprehensive object model guide
- `access-control.md` - RBAC and permission patterns
- `complete-example.md` - Full NFT collection example
