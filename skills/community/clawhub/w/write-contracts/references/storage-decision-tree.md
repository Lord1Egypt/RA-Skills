# Storage Type Decision Tree

## When to Use This

User mentions: "store", "save", "track", "registry", "mapping", "collection", "list"

## Decision Questions

### Q1: Access Pattern

**Ask:** "What's your access pattern?"

- **Sequential access** (iterate through items in order) → Vector (if <100) or SmartVector (if 100+)

- **Key-value lookups** (find item by key/address) → Table (unordered) or OrderedMap/BigOrderedMap (sorted)

- **Both** (ordered iteration + key lookup) → OrderedMap (<100) or BigOrderedMap (100+)

### Q2: Expected Size

**Ask:** "What's the expected data size?"

- **Small & bounded** (<100 items) → Vector or OrderedMap

- **Large or unbounded** (100s-1000s items) → SmartVector, Table, or BigOrderedMap

- **Unknown/unpredictable** → SmartVector or BigOrderedMap (safest, grows dynamically)

### Q3: Length Tracking (Conditional)

**Ask only if size matters:** "Do you need to track the total count?"

- **Yes, need `.length()`** → TableWithLength, OrderedMap, Vector, SmartVector

- **No, don't need count** → Table or BigOrderedMap

## Decision Flow

```
Start: User mentions storage
    |
    v
Q1: What's your access pattern?
    |
    ├─→ Sequential access
    |   |
    |   └─→ Q2: Expected size?
    |       |
    |       ├─→ <100 items → Vector<T>
    |       └─→ 100+ items → SmartVector<T>
    |
    ├─→ Key-value lookups
    |   |
    |   └─→ Q3: Need .length()?
    |       |
    |       ├─→ Yes → TableWithLength<K, V>
    |       └─→ No → Table<K, V>
    |
    └─→ Both (ordered + lookup)
        |
        └─→ Q2: Expected size?
            |
            ├─→ <100 items → OrderedMap<K, V>
            └─→ 100+ items → BigOrderedMap<K, V>
```

## Common Patterns Quick Reference

| User Says             | Access Pattern    | Size      | Recommended Storage                             |
| --------------------- | ----------------- | --------- | ----------------------------------------------- |
| "track users"         | Key-value         | Unbounded | `Table<address, UserInfo>`                      |
| "staking records"     | Key-value         | Unbounded | `Table<address, StakeInfo>`                     |
| "leaderboard"         | Ordered + lookup  | Unbounded | `BigOrderedMap<u64, address>`                   |
| "transaction log"     | Sequential        | 100+      | `SmartVector<TxRecord>`                         |
| "whitelist"           | Sequential        | <100      | `Vector<address>`                               |
| "voting records"      | Key-value + count | Unbounded | `TableWithLength<address, bool>`                |
| "config mappings"     | Ordered + lookup  | <50       | `OrderedMap<String, Value>`                     |
| "DAO proposals"       | Ordered + lookup  | Unbounded | `BigOrderedMap<u64, Proposal>`                  |
| "user NFT collection" | Sequential        | Varies    | `Vector<Object<T>>` or `SmartVector<Object<T>>` |

## Recommendation Format

Always recommend explicitly with this format:

**"For [pattern], I recommend `[Type]<K, V>` because [reason] ([gas context])"**

**Examples:**

1. **Staking records:** "For staking records, I recommend `Table<address, StakeInfo>` because you'll have unbounded
   users with concurrent staking operations (separate slots enable parallel access with per-slot gas cost)"

2. **Leaderboard:** "For leaderboard, I recommend `BigOrderedMap<u64, address>` because you need sorted iteration for
   top N players (O(log n) operations, use allocate_spare_slots for production to ensure predictable gas)"

3. **Transaction log:** "For transaction logs, I recommend `SmartVector<TransactionRecord>` because you need
   chronological append-only storage for 100+ transactions (bucket-based storage reduces gas for large datasets)"

4. **Whitelist:** "For whitelist, I recommend `Vector<address>` because you have a small bounded list (<100 addresses)
   where O(n) lookup is acceptable (most efficient for small sequential data)"

## Important Notes

- **NEVER use SmartTable** (deprecated, replaced by BigOrderedMap)
- **Vector cutoff:** Use Vector for <100 items, SmartVector for 100+
- **OrderedMap cutoff:** Use OrderedMap for <100 items, BigOrderedMap for 100+
- **Production:** For BigOrderedMap, mention `allocate_spare_slots` configuration for predictable gas
- **Gas context:** Keep to one line, focus on functional benefits first
