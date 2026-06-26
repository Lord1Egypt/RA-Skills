# Complete Example: NFT Collection

Full annotated example of an NFT collection contract using modern Move V2 patterns.

```move
module my_addr::nft_collection {
    use std::string::String;
    use std::signer;
    use std::vector;
    use aptos_framework::object::{Self, Object};

    // ============ Structs ============

    struct Collection has key {
        name: String,
        description: String,
        creator: address,
        nfts: vector<Object<NFT>>,
    }

    struct NFT has key {
        name: String,
        token_id: u64,
        collection: Object<Collection>,
        transfer_ref: object::TransferRef,
    }

    // ============ Constants ============

    const E_NOT_OWNER: u64 = 1;
    const E_NOT_CREATOR: u64 = 2;
    const E_EMPTY_NAME: u64 = 10;
    const E_NAME_TOO_LONG: u64 = 11;
    const E_ZERO_ADDRESS: u64 = 20;

    const MAX_NAME_LENGTH: u64 = 64;

    // ============ Public Entry Functions ============

    /// Create NFT collection
    public entry fun create_collection(
        creator: &signer,
        name: String,
        description: String
    ) {
        // Validate inputs
        assert!(string::length(&name) > 0, E_EMPTY_NAME);
        assert!(string::length(&name) <= MAX_NAME_LENGTH, E_NAME_TOO_LONG);

        let constructor_ref = object::create_named_object(
            creator,
            *string::bytes(&name)
        );

        let object_signer = object::generate_signer(&constructor_ref);

        move_to(&object_signer, Collection {
            name,
            description,
            creator: signer::address_of(creator),
            nfts: vector::empty(),
        });
    }

    /// Mint NFT into collection
    public entry fun mint_nft(
        creator: &signer,
        collection: Object<Collection>,
        nft_name: String,
        token_id: u64
    ) acquires Collection {
        // Verify creator owns collection
        let creator_addr = signer::address_of(creator);
        assert!(object::owner(collection) == creator_addr, E_NOT_CREATOR);

        // Validate input
        assert!(string::length(&nft_name) > 0, E_EMPTY_NAME);

        // Create NFT owned by collection
        let collection_addr = object::object_address(&collection);
        let constructor_ref = object::create_object(collection_addr);

        let transfer_ref = object::generate_transfer_ref(&constructor_ref);
        let object_signer = object::generate_signer(&constructor_ref);

        let nft_obj = object::object_from_constructor_ref<NFT>(&constructor_ref);

        move_to(&object_signer, NFT {
            name: nft_name,
            token_id,
            collection,
            transfer_ref,
        });

        // Add to collection
        let collection_data = borrow_global_mut<Collection>(collection_addr);
        vector::push_back(&mut collection_data.nfts, nft_obj);
    }

    /// Transfer NFT
    public entry fun transfer_nft(
        owner: &signer,
        nft: Object<NFT>,
        recipient: address
    ) acquires NFT {
        // Verify ownership
        assert!(object::owner(nft) == signer::address_of(owner), E_NOT_OWNER);

        // Validate recipient
        assert!(recipient != @0x0, E_ZERO_ADDRESS);

        // Transfer
        let nft_data = borrow_global<NFT>(object::object_address(&nft));
        object::transfer_with_ref(
            object::generate_linear_transfer_ref(&nft_data.transfer_ref),
            recipient
        );
    }

    // ============ Public View Functions ============

    #[view]
    public fun get_collection_size(collection: Object<Collection>): u64 acquires Collection {
        let collection_data = borrow_global<Collection>(
            object::object_address(&collection)
        );
        vector::length(&collection_data.nfts)
    }

    #[view]
    public fun get_nft_name(nft: Object<NFT>): String acquires NFT {
        let nft_data = borrow_global<NFT>(object::object_address(&nft));
        nft_data.name
    }
}
```

## Key Patterns Demonstrated

1. **Named Object for Collection**
   - Collection created with `create_named_object()` using collection name as seed
   - Allows deterministic lookup of collection

2. **Nested Ownership**
   - NFTs are owned by the collection (collection address is NFT creator)
   - Collection tracks all NFTs in a vector
   - Bidirectional reference (NFT stores parent collection)

3. **Access Control**
   - Verify creator owns collection before minting
   - Verify owner before transferring NFT
   - Clear error codes for different failure modes

4. **Input Validation**
   - Check string lengths (non-empty, not too long)
   - Validate recipient address (not @0x0)
   - Validate all inputs before state changes

5. **Transfer Management**
   - Store TransferRef in NFT struct
   - Use `generate_linear_transfer_ref()` when transferring
   - Always verify ownership before transfer

6. **View Functions**
   - Mark read-only functions with `#[view]`
   - Return data without modifying state
   - Useful for querying contract state

## Testing Recommendations

```move
#[test(creator = @0x123, user = @0x456)]
public fun test_create_and_mint(creator: &signer, user: &signer) {
    // Test collection creation
    create_collection(creator, string::utf8(b"My Collection"), string::utf8(b"Description"));

    // Get collection
    let collection_addr = object::create_object_address(&@0x123, b"My Collection");
    let collection = object::address_to_object<Collection>(collection_addr);

    // Test minting
    mint_nft(creator, collection, string::utf8(b"NFT #1"), 1);

    // Verify collection size
    assert!(get_collection_size(collection) == 1, 0);
}
```

## See Also

- `object-patterns.md` - Object creation and management patterns
- `access-control.md` - RBAC patterns
- `../../../../patterns/move/DIGITAL_ASSETS.md` - For production NFTs, use Digital Asset standard
