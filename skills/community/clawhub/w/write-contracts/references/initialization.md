# Initialization Patterns

Patterns for contract initialization using `init_module`.

## Basic init_module Pattern

```move
module marketplace_addr::marketplace {
    use std::signer;
    use aptos_framework::object::{Self, Object};

    struct MarketplaceConfig has key {
        admin: address,
        fee_percentage: u64,
        paused: bool,
    }

    // ✅ CORRECT: Private init_module for initialization
    fun init_module(deployer: &signer) {
        // Initialize global config on deployment
        let constructor_ref = object::create_named_object(
            deployer,
            b"MARKETPLACE_CONFIG_V1"
        );
        let object_signer = object::generate_signer(&constructor_ref);

        move_to(&object_signer, MarketplaceConfig {
            admin: signer::address_of(deployer),
            fee_percentage: 250, // 2.5%
            paused: false,
        });
    }

    // Access config directly using named address
    public fun get_config(): Object<MarketplaceConfig> {
        let config_addr = object::create_object_address(
            &@marketplace_addr,
            b"MARKETPLACE_CONFIG_V1"
        );
        object::address_to_object<MarketplaceConfig>(config_addr)
    }
}
```

## init_module Rules

1. **Must be private** (no `public` keyword)
2. **Must be named** `init_module` exactly
3. **Takes at most one parameter** of type `&signer` (the deployer)
4. **Called automatically** once when module is first published
5. **Cannot be called again** after deployment

## Common Patterns

### Registry Creation

```move
struct ItemRegistry has key {
    items: vector<Object<Item>>,
    admin: address,
}

fun init_module(deployer: &signer) {
    let constructor_ref = object::create_named_object(
        deployer,
        b"ITEM_REGISTRY_V1"
    );
    let object_signer = object::generate_signer(&constructor_ref);

    move_to(&object_signer, ItemRegistry {
        items: vector::empty(),
        admin: signer::address_of(deployer),
    });
}
```

## Anti-patterns

### ❌ WRONG: Public init function

```move
// ❌ DON'T: This won't be called automatically
public entry fun initialize(deployer: &signer) {
    // Requires manual call after deployment
}
```

### ❌ WRONG: Forgetting init_module

```move
// ❌ DON'T: Missing init_module means no automatic initialization
module my_addr::my_module {
    struct Config has key { value: u64 }
    // Missing init_module - Config never created!
}
```

## Best Practices

1. **Use named objects for singletons** - Makes them easily retrievable
2. **Initialize all global state** - Registries, configs, admin lists
3. **Set up admin/owner permissions** - Grant initial capabilities
4. **Keep init_module simple** - Just initial setup, not complex logic

## See Also

- `object-patterns.md` - Named object patterns
- `access-control.md` - Admin and permission setup
