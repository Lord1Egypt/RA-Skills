# Storage Patterns: Use Case → Type Mapping

## Pattern 1: User Registries

**Use Case:** Track data about many users (profiles, balances, settings) **Storage:** `Table<address, UserData>`
**Why:**

- Unbounded users
- O(1) lookup by address
- High concurrency (many users updating simultaneously)
- Separate slots enable parallel transactions

**Gas:** Per-slot cost but worth it for concurrency

**Example:**

```move
struct UserRegistry has key {
    users: Table<address, UserProfile>,
}

struct UserProfile has store {
    name: String,
    level: u64,
    balance: u64,
}

public entry fun register_user(user: &signer, name: String) acquires UserRegistry {
    let user_addr = signer::address_of(user);
    let registry = borrow_global_mut<UserRegistry>(@my_addr);

    assert!(!table::contains(&registry.users, user_addr), E_ALREADY_REGISTERED);

    table::add(&mut registry.users, user_addr, UserProfile {
        name,
        level: 1,
        balance: 0,
    });
}
```

---

## Pattern 2: Staking Records

**Use Case:** Track which users stake which assets (NFTs, tokens) **Storage:** `Table<address, StakeInfo>` **Why:**

- Unbounded stakers
- Concurrent stake/unstake operations
- No ordering needed
- Fast lookup by asset (NFT) address

**Gas:** Separate slots enable concurrent staking

**Example:**

```move
struct StakingPool has key {
    stakes: Table<address, StakeInfo>,  // NFT address → stake info
}

struct StakeInfo has store {
    owner: address,
    staked_at: u64,
    reward_debt: u64,
}

public entry fun stake_nft(
    user: &signer,
    nft: Object<AptosToken>
) acquires StakingPool {
    let nft_addr = object::object_address(&nft);
    assert!(object::owner(nft) == signer::address_of(user), E_NOT_OWNER);

    let pool = borrow_global_mut<StakingPool>(@my_addr);
    assert!(!table::contains(&pool.stakes, nft_addr), E_ALREADY_STAKED);

    table::add(&mut pool.stakes, nft_addr, StakeInfo {
        owner: signer::address_of(user),
        staked_at: timestamp::now_seconds(),
        reward_debt: 0,
    });
}
```

---

## Pattern 3: Leaderboards / Rankings

**Use Case:** Sorted list by score, rank, or timestamp **Storage:** `BigOrderedMap<u64, address>` (score → player)
**Why:**

- Need sorted iteration (top 10, top 100)
- Unbounded players
- O(log n) insertion and lookup

**Gas:** Use `allocate_spare_slots` for production predictability

**Production tip:** Pre-allocate slots for consistent gas

**Example:**

```move
struct Leaderboard has key {
    scores: BigOrderedMap<u64, address>,  // score → player
}

fun init_module(deployer: &signer) {
    let scores = big_ordered_map::new_with_config<u64, address>(
        100,  // initial capacity
        true, // allocate_spare_slots
        true  // reuse_slots
    );
    move_to(deployer, Leaderboard { scores });
}

// Iterate top 10: iterate from max score
public fun get_top_10(): vector<address> acquires Leaderboard {
    let leaderboard = borrow_global<Leaderboard>(@my_addr);
    let top = vector[];
    let count = 0;

    big_ordered_map::for_each_reverse(&leaderboard.scores, |_score, player| {
        if (count < 10) {
            vector::push_back(&mut top, *player);
            count = count + 1;
        }
    });

    top
}
```

---

## Pattern 4: Transaction Logs

**Use Case:** Chronological append-only records **Storage:** `SmartVector<TransactionRecord>` (if 100+) or `Vector<T>`
(if <100) **Why:**

- Sequential access
- Append-only operations
- SmartVector scales to 1000s efficiently

**Gas:** Vector efficient for small, SmartVector better for large

**Size threshold:** ~100 items

**Example:**

```move
struct AuditLog has key {
    transactions: SmartVector<TxRecord>,  // For 100+ transactions
}

struct TxRecord has store {
    timestamp: u64,
    action: String,
    executor: address,
    amount: u64,
}

public entry fun log_transaction(
    action: String,
    executor: address,
    amount: u64
) acquires AuditLog {
    let log = borrow_global_mut<AuditLog>(@my_addr);
    smart_vector::push_back(&mut log.transactions, TxRecord {
        timestamp: timestamp::now_seconds(),
        action,
        executor,
        amount,
    });
}
```

---

## Pattern 5: Small Config Mappings

**Use Case:** Feature flags, settings (<50 items) **Storage:** `OrderedMap<String, ConfigValue>` **Why:**

- Small bounded data
- Sorted iteration helpful
- Single-slot efficiency (65μs vs 123μs for BigOrderedMap)

**Gas:** Most efficient for small sorted data

**Example:**

```move
struct Config has key {
    settings: OrderedMap<String, bool>,  // feature flags
}

public entry fun set_feature(
    admin: &signer,
    feature: String,
    enabled: bool
) acquires Config {
    assert!(signer::address_of(admin) == @my_addr, E_UNAUTHORIZED);

    let config = borrow_global_mut<Config>(@my_addr);
    if (ordered_map::contains(&config.settings, &feature)) {
        *ordered_map::borrow_mut(&mut config.settings, &feature) = enabled;
    } else {
        ordered_map::add(&mut config.settings, feature, enabled);
    }
}
```

---

## Pattern 6: DAO Proposals

**Use Case:** Governance proposals with IDs **Storage:** `BigOrderedMap<u64, Proposal>` **Why:**

- Iterate recent proposals (by ID or timestamp)
- Unbounded growth
- Ordered by proposal ID

**Gas:** Predictable with pre-allocation

**Example:**

```move
struct DAO has key {
    proposals: BigOrderedMap<u64, Proposal>,
    next_proposal_id: u64,
}

struct Proposal has store {
    proposer: address,
    description: String,
    votes_for: u64,
    votes_against: u64,
    created_at: u64,
}

public entry fun create_proposal(
    proposer: &signer,
    description: String
) acquires DAO {
    let dao = borrow_global_mut<DAO>(@my_addr);
    let proposal_id = dao.next_proposal_id;
    dao.next_proposal_id = proposal_id + 1;

    big_ordered_map::add(&mut dao.proposals, proposal_id, Proposal {
        proposer: signer::address_of(proposer),
        description,
        votes_for: 0,
        votes_against: 0,
        created_at: timestamp::now_seconds(),
    });
}
```

---

## Pattern 7: Whitelists / Blacklists

**Use Case:** Small list of addresses (<100) **Storage:** `Vector<address>` **Why:**

- Bounded size
- Simple iteration
- O(n) lookup acceptable for small lists

**Gas:** Most efficient for small address lists

**Example:**

```move
struct AccessControl has key {
    admins: vector<address>,  // Small admin list
}

public entry fun add_admin(owner: &signer, new_admin: address) acquires AccessControl {
    assert!(signer::address_of(owner) == @my_addr, E_UNAUTHORIZED);

    let access = borrow_global_mut<AccessControl>(@my_addr);
    assert!(!vector::contains(&access.admins, &new_admin), E_ALREADY_ADMIN);

    vector::push_back(&mut access.admins, new_admin);
}

public fun is_admin(user: address): bool acquires AccessControl {
    let access = borrow_global<AccessControl>(@my_addr);
    vector::contains(&access.admins, &user)
}
```

---

## Pattern 8: Voting Records

**Use Case:** Track who voted on a proposal **Storage:** `Table<address, bool>` or `TableWithLength<address, bool>`
**Why:**

- Unbounded voters
- Concurrent voting
- Use TableWithLength if you need vote count

**Gas:** Concurrent voting without conflicts

**Example:**

```move
struct Proposal has store {
    voters: TableWithLength<address, bool>,
    description: String,
}

public entry fun vote(
    voter: &signer,
    proposal_id: u64,
    vote: bool
) acquires ProposalRegistry {
    let voter_addr = signer::address_of(voter);
    let proposal = get_proposal_mut(proposal_id);

    assert!(!table_with_length::contains(&proposal.voters, voter_addr), E_ALREADY_VOTED);

    table_with_length::add(&mut proposal.voters, voter_addr, vote);
}

public fun get_vote_count(proposal_id: u64): u64 acquires ProposalRegistry {
    let proposal = get_proposal(proposal_id);
    table_with_length::length(&proposal.voters)
}
```

---

## Pattern 9: Asset Collections

**Use Case:** User's NFT collection, token holdings **Storage:** `Vector<Object<T>>` (<100) or `SmartVector<Object<T>>`
(100+) **Why:**

- Sequential access (show user's NFTs)
- Append when acquired, swap_remove when transferred

**Gas:** Vector efficient for most users, SmartVector for collectors

**Example:**

```move
struct Collection has key {
    nfts: vector<Object<AptosToken>>,  // Most users have <100 NFTs
}

public entry fun add_nft_to_collection(
    owner: &signer,
    nft: Object<AptosToken>
) acquires Collection {
    assert!(object::owner(nft) == signer::address_of(owner), E_NOT_OWNER);

    let collection = borrow_global_mut<Collection>(signer::address_of(owner));
    vector::push_back(&mut collection.nfts, nft);
}

// Remove NFT efficiently with swap_remove (O(1) instead of O(n))
public entry fun remove_nft_from_collection(
    owner: &signer,
    nft: Object<AptosToken>
) acquires Collection {
    let collection = borrow_global_mut<Collection>(signer::address_of(owner));
    let (found, index) = vector::index_of(&collection.nfts, &nft);

    assert!(found, E_NFT_NOT_FOUND);

    vector::swap_remove(&mut collection.nfts, index);
}
```

---

## Quick Pattern Reference

| Pattern          | Storage                              | Size      | Concurrent | Ordered |
| ---------------- | ------------------------------------ | --------- | ---------- | ------- |
| User registry    | `Table<address, UserInfo>`           | Unbounded | ✓          | ✗       |
| Staking          | `Table<address, StakeInfo>`          | Unbounded | ✓          | ✗       |
| Leaderboard      | `BigOrderedMap<u64, address>`        | Unbounded | ~          | ✓       |
| Transaction log  | `SmartVector<TxRecord>`              | 100+      | ✗          | ✓       |
| Small config     | `OrderedMap<String, Value>`          | <50       | ✗          | ✓       |
| DAO proposals    | `BigOrderedMap<u64, Proposal>`       | Unbounded | ~          | ✓       |
| Whitelist        | `Vector<address>`                    | <100      | ✗          | ✓       |
| Voting           | `TableWithLength<address, bool>`     | Unbounded | ✓          | ✗       |
| Asset collection | `Vector<Object<T>>` or `SmartVector` | Varies    | ✗          | ✓       |

## When to Use Each Pattern

### High Concurrency Required

- User registry (many users updating profiles simultaneously)
- Staking (many users staking/unstaking concurrently)
- Voting (many voters casting votes during window)
- → Use **Table** or **TableWithLength**

### Ordered Iteration Required

- Leaderboard (top N by score)
- Recent proposals (latest first)
- Transaction history (chronological)
- → Use **BigOrderedMap**, **SmartVector**, or **OrderedMap**

### Small & Bounded Data

- Admin whitelist (<10 addresses)
- Feature flags (<50 settings)
- → Use **Vector** or **OrderedMap**

### Large & Unbounded Data

- User registry (thousands of users)
- Transaction logs (continuous growth)
- Leaderboard (unlimited players)
- → Use **Table**, **SmartVector**, or **BigOrderedMap**

### Need Count/Length

- Vote counting
- Total users
- Total transactions
- → Use **TableWithLength**, **Vector**, **SmartVector**, or **OrderedMap** (all have `.length()`)
