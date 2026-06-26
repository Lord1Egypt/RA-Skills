# Storage Gas Optimization

## Gas Cost Fundamentals

**Key insight:** "Writing to a new slot incurs the highest storage fee"

### Cost Hierarchy (Highest to Lowest)

1. **New slot creation** (most expensive)
2. **Writing to existing slot**
3. **Reading from slot**
4. **Slot deletion** (provides refund)

### Storage Pricing Model

**From Aptos Documentation:**

- **Per-slot cost:** Each unique storage location (key-value pair) requires slot allocation
- **Refunds:** Deleting data provides storage refunds
- **Concurrent access:** Separate slots enable parallel transaction execution

## Type-Specific Gas Characteristics

### Table / TableWithLength

**Cost:** Per-slot gas for each entry **Benefit:** Enables concurrent access (parallel transactions) **Trade-off:**
Higher cost per entry, but worth it for concurrency

**Why separate slots matter:**

```move
// Two users updating different entries → Can run in parallel
table::add(&mut registry.users, alice, alice_data);  // Slot 1
table::add(&mut registry.users, bob, bob_data);      // Slot 2 (parallel!)
```

**Optimization:** Batch operations when possible

```move
// Batch user registrations in single transaction
public entry fun batch_register(users: vector<address>) {
    vector::for_each(users, |user| {
        table::add(&mut registry.users, user, default_data);
    });
}
```

---

### BigOrderedMap

**Default:** Dynamic slot allocation **Optimization:** Use configuration for predictable gas

**Production Configuration:**

```move
// Production configuration for predictable gas
let map = big_ordered_map::new_with_config<K, V>(
    /* initial_capacity */ 100,
    /* allocate_spare_slots */ true,   // Pre-allocate for predictable gas
    /* reuse_slots */ true              // Reuse freed slots (no refund, but consistent cost)
);
```

**Why this matters:**

- `allocate_spare_slots`: Pre-allocates storage, avoiding variable gas for growth
- `reuse_slots`: Keeps slots after removal, prevents refund but ensures predictable insert costs

**Gas impact:**

- **Without config:** First insert cheap, growth insertions expensive (unpredictable)
- **With config:** Consistent costs for all operations (predictable for production)

**Example:**

```move
struct Leaderboard has key {
    scores: BigOrderedMap<u64, address>,
}

fun init_module(deployer: &signer) {
    // Configure for 100+ expected players
    let scores = big_ordered_map::new_with_config<u64, address>(
        100,  // Initial capacity
        true, // Allocate spare slots
        true  // Reuse slots
    );

    move_to(deployer, Leaderboard { scores });
}
```

---

### Vector vs SmartVector

**Vector:** Contiguous storage, efficient for small data **SmartVector:** Bucket-based, 1.5-2x overhead for small data,
but scales better

**Cutoff:** ~100 items

**Gas comparison:**

```
Vector (10 items):        ~50-60μs
SmartVector (10 items):   ~75-100μs (1.5-2x overhead)

Vector (1000 items):      Can become expensive in single slot
SmartVector (1000 items): Distributed across buckets, more predictable
```

**When overhead is worth it:**

- Data may grow beyond 100 items
- Append-heavy workloads
- Unpredictable final size

**Example decision:**

```move
// User admin list - use Vector (small, bounded)
struct AccessControl has key {
    admins: vector<address>,  // Expect <20 admins
}

// Transaction log - use SmartVector (large, growing)
struct AuditLog has key {
    transactions: SmartVector<TxRecord>,  // Could reach 1000s
}
```

---

### OrderedMap vs BigOrderedMap

**Small data performance:**

- OrderedMap (10 items): 65μs
- BigOrderedMap (10 items): 123μs (1.9x overhead)

**Why the overhead?**

- OrderedMap: Single slot, sorted vector
- BigOrderedMap: B+ tree, dynamic growth infrastructure

**When overhead is worth it:**

- Data may grow unbounded
- Need predictable performance at scale
- Unknown final size

**Example decision:**

```move
// Feature flags - use OrderedMap (small, bounded)
struct Config has key {
    settings: OrderedMap<String, bool>,  // <50 flags
}

// DAO proposals - use BigOrderedMap (unbounded)
struct DAO has key {
    proposals: BigOrderedMap<u64, Proposal>,  // Could reach 1000s
}
```

---

## Optimization Strategies

### 1. Choose the Right Size

**Small & bounded (<100 items):**

- Vector
- OrderedMap
- Single-slot efficiency

**Large or unbounded (100+ items):**

- SmartVector
- Table
- BigOrderedMap
- Scalable structures

**Unknown/unpredictable:**

- SmartVector or BigOrderedMap
- Safe, grows dynamically

---

### 2. Batch Operations

**Bad: Multiple separate operations**

```move
table::add(&mut map, key1, value1);  // Write to map
table::add(&mut map, key2, value2);  // Write to map again
table::add(&mut map, key3, value3);  // Write to map again
```

**Better: Batch if possible**

```move
public entry fun batch_add(keys: vector<K>, values: vector<V>) {
    let len = vector::length(&keys);
    let i = 0;
    while (i < len) {
        table::add(&mut map, keys[i], values[i]);
        i = i + 1;
    };
}
```

**Note:** Batching reduces transaction overhead but doesn't reduce per-slot costs

---

### 3. Pre-allocate for Production

**For BigOrderedMap in high-value contracts:**

```move
// Good: Pre-configured for predictable gas
let leaderboard = big_ordered_map::new_with_config<u64, address>(
    100,    // Expected capacity
    true,   // Allocate spare slots
    true    // Reuse slots
);
// Predictable gas even as users join/leave
```

**For other types:**

- Vector: Consider `vector::reserve()` if final size is known
- SmartVector: Already optimized with buckets
- Table: No pre-allocation needed (separate slots)

---

### 4. Use swap_remove for Vectors

**O(n) - shifts all elements:**

```move
vector::remove(&mut vec, index);
// [a, b, c, d] remove index 1 → [a, c, d]
// Requires shifting c and d left
```

**O(1) - swaps with last element, then removes:**

```move
vector::swap_remove(&mut vec, index);
// [a, b, c, d] swap_remove index 1 → [a, d, c]
// Swaps b with d, then removes last position
```

**When to use swap_remove:**

- Order doesn't matter (user collections, registries)
- Frequent removals
- Gas efficiency critical

**Example:**

```move
// User NFT collection - order doesn't matter
public entry fun remove_nft(owner: &signer, nft: Object<Token>) acquires Collection {
    let collection = borrow_global_mut<Collection>(signer::address_of(owner));
    let (found, index) = vector::index_of(&collection.nfts, &nft);

    assert!(found, E_NFT_NOT_FOUND);

    // O(1) removal - order doesn't matter for collections
    vector::swap_remove(&mut collection.nfts, index);
}
```

---

### 5. Minimize Storage Writes

**Read before write:**

```move
// Good: Only write if value changes
let current = table::borrow(&map, key);
if (*current != new_value) {
    *table::borrow_mut(&mut map, key) = new_value;
}

// Bad: Always write (even if same value)
*table::borrow_mut(&mut map, key) = new_value;
```

**Use events instead of storage for historical data:**

```move
// Bad: Store all transfers in vector (expensive)
struct TransferHistory has key {
    transfers: SmartVector<Transfer>,
}

// Good: Emit events (cheaper, queryable off-chain)
#[event]
struct TransferEvent has drop, store {
    from: address,
    to: address,
    amount: u64,
}

public entry fun transfer(from: &signer, to: address, amount: u64) {
    // ... transfer logic ...

    // Emit event (cheaper than storage)
    event::emit(TransferEvent { from: signer::address_of(from), to, amount });
}
```

---

## Gas Profiling Commands

### Local Testing

```bash
# Profile gas usage
aptos move test --gas-profiling

# Local simulation with gas estimation
aptos move run --local --gas-unit-price 100

# Profile specific function
aptos move test --filter test_function_name --gas-profiling
```

### Testnet Testing

```bash
# Deploy to testnet
aptos move publish --profile testnet

# Run function and check gas
aptos move run \
  --function-id 'default::module::function' \
  --args address:0x123 \
  --profile testnet \
  --gas-unit-price 100 \
  --max-gas 10000
```

---

## Quick Decision: Gas Priority

### If gas predictability is CRITICAL

**DAO, high-value contracts:**

- Use BigOrderedMap with `allocate_spare_slots` for ordered data
- Use Table for unordered data (separate slots already predictable)
- Configure for worst-case capacity

**Example:**

```move
// DAO with predictable gas
fun init_module(deployer: &signer) {
    let proposals = big_ordered_map::new_with_config<u64, Proposal>(
        1000,  // Worst-case capacity
        true,  // Allocate spare slots
        true   // Reuse slots
    );
    move_to(deployer, DAO { proposals, next_id: 0 });
}
```

---

### If gas efficiency is CRITICAL

**High-frequency operations:**

- Use Vector/OrderedMap for small bounded data
- Use SmartVector/Table for large data
- Minimize writes, batch operations

**Example:**

```move
// High-frequency admin checks
struct AccessControl has key {
    admins: vector<address>,  // Small bounded list for O(1) iteration
}

public fun is_admin(user: address): bool acquires AccessControl {
    let access = borrow_global<AccessControl>(@my_addr);
    vector::contains(&access.admins, &user)  // Fast for <20 admins
}
```

---

### If unsure

**Safe defaults:**

- Use SmartVector or BigOrderedMap
- Safe, grows dynamically
- Reasonable gas characteristics

**Example:**

```move
// Unknown final size - use SmartVector
struct EventLog has key {
    events: SmartVector<Event>,  // May grow to 100s or 1000s
}
```

---

## Gas Optimization Checklist

- [ ] **Storage type matches access pattern** (sequential vs lookup vs ordered)
- [ ] **Size threshold correct** (<100 vs 100+)
- [ ] **BigOrderedMap configured for production** (if used)
- [ ] **Using swap_remove for unordered vectors** (if order doesn't matter)
- [ ] **Batching operations when possible** (reduce transaction overhead)
- [ ] **Events used for historical data** (cheaper than storage)
- [ ] **Minimizing writes** (only write if value changes)
- [ ] **Gas profiling done** (test with realistic data sizes)

---

## Common Gas Mistakes

### ❌ Mistake 1: Using Vector for unbounded data

```move
// Bad: Vector for unlimited users
struct UserRegistry has key {
    users: vector<UserInfo>,  // Could grow to 1000s!
}
```

**Impact:** High gas for large vectors, potential failure

**Fix:** Use Table or SmartVector

---

### ❌ Mistake 2: Not pre-allocating BigOrderedMap

```move
// Bad: Default config for production leaderboard
let leaderboard = big_ordered_map::new<u64, address>();
```

**Impact:** Unpredictable gas during growth

**Fix:** Use `new_with_config` with spare slots

---

### ❌ Mistake 3: Storing history on-chain

```move
// Bad: All transactions in storage
struct History has key {
    transactions: SmartVector<Transfer>,  // Growing forever
}
```

**Impact:** Ever-growing storage costs

**Fix:** Use events for history, storage for current state

---

### ❌ Mistake 4: Using remove instead of swap_remove

```move
// Bad: O(n) removal
vector::remove(&mut collection.nfts, index);
```

**Impact:** High gas for large collections

**Fix:** Use `swap_remove` when order doesn't matter

---

### ❌ Mistake 5: Wrong type for use case

```move
// Bad: Vector for key-value lookups
struct UserRegistry has key {
    users: vector<UserInfo>,  // Need to iterate to find user!
}

public fun get_user(addr: address): UserInfo {
    // O(n) search through vector
    vector::find(&users, |u| u.address == addr)
}
```

**Impact:** O(n) instead of O(1) lookups

**Fix:** Use Table for key-value data

---

## Resources

**Official Documentation:**

- [Gas and Storage Fees](https://aptos.dev/network/blockchain/gas-txn-fee)
- [Aptos Gas Schedule](https://github.com/aptos-labs/aptos-core/blob/main/aptos-gas-schedule/src/gas_schedule.rs)

**Tools:**

- `aptos move test --gas-profiling`
- [Aptos Explorer](https://explorer.aptoslabs.com) - View transaction gas costs
