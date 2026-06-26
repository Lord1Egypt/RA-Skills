# Storage Type Reference

## Vector

**What:** Ordered array, dynamic sizing **Performance:** O(1) append/access, O(n) middle insertion **Size limit:**
Unbounded but best for <100 items **Gas:** Efficient for small data, direct storage access **When:** Sequential access,
small collections, simple iteration **Example:** `Vector<address>` for admin whitelist

**Code Example:**

```move
use std::vector;

struct Whitelist has key {
    admins: vector<address>,
}

public entry fun add_admin(owner: &signer, new_admin: address) acquires Whitelist {
    let whitelist = borrow_global_mut<Whitelist>(signer::address_of(owner));
    vector::push_back(&mut whitelist.admins, new_admin);
}

// O(n) search acceptable for small lists
public fun is_admin(user: address): bool acquires Whitelist {
    let whitelist = borrow_global<Whitelist>(@my_addr);
    vector::contains(&whitelist.admins, &user)
}
```

---

## SmartVector

**What:** Scalable vector with bucket-based storage **Performance:** O(1) append/pop, O(n) middle operations **Size
limit:** Unbounded, scales to 1000s **Gas:** 1.5-2x overhead vs Vector for small data, better for large **When:**
Sequential access, 100+ items, append-heavy workloads **Example:** `SmartVector<TransactionRecord>` for logs **Note:**
Use Vector for <100, SmartVector for 100+

**Code Example:**

```move
use aptos_std::smart_vector::{Self, SmartVector};

struct TransactionLog has key {
    transactions: SmartVector<TransactionRecord>,
}

struct TransactionRecord has store {
    timestamp: u64,
    amount: u64,
    from: address,
    to: address,
}

public entry fun log_transaction(
    timestamp: u64,
    amount: u64,
    from: address,
    to: address
) acquires TransactionLog {
    let log = borrow_global_mut<TransactionLog>(@my_addr);
    smart_vector::push_back(&mut log.transactions, TransactionRecord {
        timestamp,
        amount,
        from,
        to,
    });
}
```

---

## Table

**What:** Unordered key-value map, separate slots per entry **Performance:** O(1) lookup, insert, remove **Size limit:**
Unbounded **Gas:** Per-slot storage cost, enables concurrent access **When:** Unbounded key-value data, high
concurrency, no ordering **Example:** `Table<address, UserInfo>` for user registry **Note:** No `.length()` - use
TableWithLength if needed

**Code Example:**

```move
use aptos_std::table::{Self, Table};

struct UserRegistry has key {
    users: Table<address, UserInfo>,
}

struct UserInfo has store {
    name: String,
    balance: u64,
}

public entry fun register_user(user: &signer, name: String) acquires UserRegistry {
    let user_addr = signer::address_of(user);
    let registry = borrow_global_mut<UserRegistry>(@my_addr);

    assert!(!table::contains(&registry.users, user_addr), E_ALREADY_REGISTERED);

    table::add(&mut registry.users, user_addr, UserInfo {
        name,
        balance: 0,
    });
}
```

---

## TableWithLength

**What:** Table with length tracking **Performance:** Same as Table **Size limit:** Unbounded **Gas:** Small overhead
for tracking count **When:** Need `.length()` for Table use case **Example:** `TableWithLength<address, Ballot>` for
vote counting

**Code Example:**

```move
use aptos_std::table_with_length::{Self, TableWithLength};

struct Proposal has store {
    voters: TableWithLength<address, bool>,
    description: String,
}

public entry fun vote(voter: &signer, proposal_id: u64) acquires ProposalRegistry {
    let voter_addr = signer::address_of(voter);
    let proposal = get_proposal_mut(proposal_id);

    assert!(!table_with_length::contains(&proposal.voters, voter_addr), E_ALREADY_VOTED);

    table_with_length::add(&mut proposal.voters, voter_addr, true);
}

public fun get_vote_count(proposal_id: u64): u64 acquires ProposalRegistry {
    let proposal = get_proposal(proposal_id);
    table_with_length::length(&proposal.voters)
}
```

---

## OrderedMap

**What:** Small sorted map, single slot storage **Performance:** O(log n) operations, sorted iteration **Size limit:**
<100 items recommended **Gas:** 65μs for 10 items, single-slot efficiency **When:** Small bounded data needing sorted
access **Example:** `OrderedMap<String, ConfigValue>` for feature flags

**Code Example:**

```move
use aptos_std::ordered_map::{Self, OrderedMap};

struct Config has key {
    settings: OrderedMap<String, bool>,
}

public entry fun set_feature_flag(admin: &signer, feature: String, enabled: bool) acquires Config {
    // ✅ ALWAYS: Verify admin authorization
    assert!(signer::address_of(admin) == @my_addr, E_UNAUTHORIZED);

    let config = borrow_global_mut<Config>(@my_addr);

    if (ordered_map::contains(&config.settings, &feature)) {
        *ordered_map::borrow_mut(&mut config.settings, &feature) = enabled;
    } else {
        ordered_map::add(&mut config.settings, feature, enabled);
    }
}

// Iterate over all settings in sorted order
public fun list_features(): vector<String> acquires Config {
    let config = borrow_global<Config>(@my_addr);
    let features = vector[];

    ordered_map::for_each_ref(&config.settings, |key, _value| {
        vector::push_back(&mut features, *key);
    });

    features
}
```

---

## BigOrderedMap

**What:** Large sorted map, B+ tree implementation **Performance:** O(log n) operations, scales unbounded **Size
limit:** Unbounded, grows dynamically **Gas:** Predictable with allocate_spare_slots configuration **When:** Unbounded
sorted data, ordered iteration **Example:** `BigOrderedMap<u64, PlayerData>` for leaderboards **Production:** Use
`allocate_spare_slots` + `reuse_slots` for predictable gas

**Code Example:**

```move
use aptos_std::big_ordered_map::{Self, BigOrderedMap};

struct Leaderboard has key {
    scores: BigOrderedMap<u64, address>,  // score -> player
}

fun init_module(deployer: &signer) {
    // Production configuration for predictable gas
    let scores = big_ordered_map::new_with_config<u64, address>(
        100,    // initial_capacity
        true,   // allocate_spare_slots - pre-allocate for predictable gas
        true    // reuse_slots - reuse freed slots for consistent costs
    );

    move_to(deployer, Leaderboard { scores });
}

public entry fun update_score(player: &signer, new_score: u64) acquires Leaderboard {
    let player_addr = signer::address_of(player);
    let leaderboard = borrow_global_mut<Leaderboard>(@my_addr);

    // Find old score to remove (collect key first to avoid nested borrow)
    let old_score_opt = option::none<u64>();
    big_ordered_map::for_each_ref(&leaderboard.scores, |score, addr| {
        if (*addr == player_addr) {
            old_score_opt = option::some(*score);
        }
    });

    // Remove old score if exists
    if (option::is_some(&old_score_opt)) {
        big_ordered_map::remove(&mut leaderboard.scores, option::extract(&mut old_score_opt));
    };

    // Add new score
    big_ordered_map::add(&mut leaderboard.scores, new_score, player_addr);
}

// Get top N players (iterate from max score)
public fun get_top_players(n: u64): vector<address> acquires Leaderboard {
    let leaderboard = borrow_global<Leaderboard>(@my_addr);
    let top_players = vector[];
    let count = 0;

    // Iterate in descending order
    big_ordered_map::for_each_reverse(&leaderboard.scores, |_score, player| {
        if (count < n) {
            vector::push_back(&mut top_players, *player);
            count = count + 1;
        }
    });

    top_players
}
```

---

## ~~SmartTable~~ (DEPRECATED)

**Status:** Replaced by BigOrderedMap **Migration:** Use BigOrderedMap instead **Never use SmartTable in new contracts**

If you see SmartTable in existing code, migrate to BigOrderedMap:

```move
// OLD (deprecated)
use aptos_std::smart_table::{Self, SmartTable};
let table = smart_table::new<K, V>();

// NEW (use instead)
use aptos_std::big_ordered_map::{Self, BigOrderedMap};
let map = big_ordered_map::new<K, V>();
```

---

## Quick Comparison Table

| Type            | Ordered | Size      | Concurrency | .length() | Best For          |
| --------------- | ------- | --------- | ----------- | --------- | ----------------- |
| Vector          | ✓       | <100      | Low         | ✓         | Small sequential  |
| SmartVector     | ✓       | 100+      | Low         | ✓         | Large sequential  |
| Table           | ✗       | Unbounded | High        | ✗         | Unordered lookups |
| TableWithLength | ✗       | Unbounded | High        | ✓         | Lookups + count   |
| OrderedMap      | ✓       | <100      | Low         | ✓         | Small sorted      |
| BigOrderedMap   | ✓       | Unbounded | Medium      | ✗         | Large sorted      |

## Import Statements

```move
// Vector (std library)
use std::vector;

// SmartVector
use aptos_std::smart_vector::{Self, SmartVector};

// Table
use aptos_std::table::{Self, Table};

// TableWithLength
use aptos_std::table_with_length::{Self, TableWithLength};

// OrderedMap
use aptos_std::ordered_map::{Self, OrderedMap};

// BigOrderedMap
use aptos_std::big_ordered_map::{Self, BigOrderedMap};
```
