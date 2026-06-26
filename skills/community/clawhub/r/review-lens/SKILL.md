---
name: review-lens
version: 1.0.0
description: >
  Finds what human code reviewers miss — not style issues or formatting,
  but logical errors, silent edge cases, performance cliffs, implicit
  assumptions, and the bugs that hide in code that "looks right." The
  difference between "this code works" and "this code is correct."
author: J. DeVere Cooley
category: everyday-tools
tags:
  - code-review
  - quality
  - bugs
  - correctness
metadata:
  openclaw:
    emoji: "🔍"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - everyday
      - quality
---

# Review Lens

> "A code review that only checks style is a spell-check on a ransom note. The grammar is fine — the content is the problem."

## What It Does

Human reviewers are good at catching style issues, obvious bugs, and high-level design problems. They're bad at catching:

- The **edge case** that happens once per million requests but corrupts data when it does
- The **off-by-one** hiding in a `<=` that should be `<`
- The **race condition** between two operations that are "always fast enough"
- The **silent failure** where an error is caught, logged, and then... the function continues as if nothing happened
- The **implicit assumption** that the input is always sorted, always non-empty, always UTF-8

Review Lens examines code through seven specialized lenses that catch what humans skim over.

## The Seven Lenses

### Lens 1: Boundary Analysis
**Question:** What happens at the edges?

```
CHECKS:
├── Empty inputs: What if the array is []? The string is ""? The map is {}?
├── Single element: What if there's exactly one item?
├── Maximum inputs: What if there are millions of items?
├── Null/undefined: What if any parameter is nil?
├── Zero values: What if a number is 0? Negative? NaN? Infinity?
├── Unicode: What if the string contains emoji, RTL, or zero-width chars?
├── Concurrent: What if this is called simultaneously by two threads?
└── Time: What if this runs at midnight? On Feb 29? During DST transition?
```

**What it catches:**
```javascript
// Human reviewer: "Looks good, calculates average correctly"
function average(numbers) {
  return numbers.reduce((a, b) => a + b) / numbers.length;
}
// Review Lens: "Empty array → reduce throws TypeError.
// Single element → works.
// Very large array → potential floating point accumulation error.
// Array with NaN → result is NaN (silent corruption)."
```

### Lens 2: Failure Path Analysis
**Question:** When this fails, what happens?

```
CHECKS:
├── Is every error caught? (not just the expected ones)
├── When an error IS caught, does the function still behave correctly?
│   └── Does it return a sensible value? Or does it return undefined/null?
├── Are error messages useful? (contain context, not just "something went wrong")
├── Is the error propagated correctly? (not swallowed, not double-handled)
├── Are side effects cleaned up on failure? (transactions rolled back, files closed, locks released)
└── Can the caller distinguish between "no result" and "error"?
```

**What it catches:**
```python
# Human reviewer: "Good, handles the error case"
try:
    user = db.get_user(user_id)
except DatabaseError:
    logger.error("Failed to get user")
    return None

# Review Lens: "Caller receives None for BOTH 'user not found'
# AND 'database is down'. These are fundamentally different
# conditions. The caller can't distinguish a missing user from
# a system failure. Also: what if user_id is logged and contains
# PII — is the log destination PII-compliant?"
```

### Lens 3: State Transition Analysis
**Question:** Can this code reach an invalid state?

```
CHECKS:
├── Are all state transitions valid? (no invalid intermediate states)
├── Is state updated atomically? (no half-updated state visible to others)
├── Can state transitions happen out of order?
├── Are there states that can never be exited? (deadlocks, infinite loops)
├── Is cleanup guaranteed? (finally blocks, defer, destructors)
└── Are boolean flags used correctly? (not multiple booleans creating invalid combinations)
```

**What it catches:**
```java
// Human reviewer: "Order state machine, looks complete"
order.setStatus("processing");
payment.charge(order.getTotal());
order.setStatus("paid");
inventory.reserve(order.getItems());
order.setStatus("confirmed");

// Review Lens: "If payment.charge() succeeds but inventory.reserve()
// fails, the order is stuck in 'paid' state with no inventory.
// Customer is charged but order can't be fulfilled. No rollback
// mechanism. Also: between setStatus('processing') and charge(),
// the order is in a state where it appears processing but hasn't
// been charged — if the process crashes here, it stays 'processing'
// forever with no retry mechanism."
```

### Lens 4: Implicit Assumption Analysis
**Question:** What must be true for this code to work?

```
CHECKS:
├── Ordering assumptions: Does this assume input is sorted?
├── Uniqueness assumptions: Does this assume no duplicates?
├── Format assumptions: Does this assume a specific encoding, locale, timezone?
├── Size assumptions: Does this assume the data fits in memory?
├── Timing assumptions: Does this assume an operation completes "fast enough"?
├── Environment assumptions: Does this assume specific OS, permissions, or network?
├── Dependency assumptions: Does this assume a specific version of a library?
└── Business assumptions: Does this assume a rule that might change?
```

**What it catches:**
```go
// Human reviewer: "Clean function, well-structured"
func findUser(email string) (*User, error) {
    results, err := db.Query("SELECT * FROM users WHERE email = ?", email)
    if err != nil {
        return nil, err
    }
    return results[0], nil  // Return first match
}

// Review Lens: "Assumes email is unique (no UNIQUE constraint checked).
// Assumes at least one result exists (panics on empty results[0]).
// Assumes case-sensitivity matches DB collation.
// Assumes email is trimmed (trailing spaces could cause mismatch).
// SELECT * pulls all columns — schema changes break the struct mapping."
```

### Lens 5: Performance Cliff Analysis
**Question:** Where does this go from fast to catastrophic?

```
CHECKS:
├── N+1 queries: Loop that makes a DB call per iteration
├── Unbounded growth: Collections that grow without limit
├── Missing pagination: Queries that return ALL results
├── Quadratic (or worse) algorithms: Nested loops over the same data
├── Unnecessary allocations: Creating objects in hot loops
├── Missing short-circuits: Expensive operations that could bail early
├── Serialization: Serializing large objects for every request
└── Regex: Catastrophic backtracking patterns
```

**What it catches:**
```javascript
// Human reviewer: "Gets all active users and their orders, looks fine"
async function getActiveUsersWithOrders() {
  const users = await db.query('SELECT * FROM users WHERE active = true');
  for (const user of users) {
    user.orders = await db.query('SELECT * FROM orders WHERE user_id = ?', user.id);
  }
  return users;
}

// Review Lens: "N+1 query pattern. With 100 users: 101 queries.
// With 10,000 users: 10,001 queries. No pagination — loads ALL
// active users into memory. All columns selected for both tables.
// At scale: 10-second response time, potential OOM, DB connection
// pool exhaustion. Works fine in dev with 12 test users."
```

### Lens 6: Security Surface Analysis
**Question:** Where can this be abused?

```
CHECKS:
├── Input trust: Is user input validated before use?
├── Output encoding: Is output escaped for the destination context?
├── Authentication: Is the caller's identity verified?
├── Authorization: Is the caller allowed to do this specific thing?
├── Injection: Can user input alter queries, commands, or templates?
├── Information leak: Do error messages expose internal details?
├── Timing: Can response times reveal secrets?
└── TOCTOU: Is there a gap between checking permission and performing action?
```

### Lens 7: Correctness Under Change
**Question:** How easily can a future change break this code's assumptions?

```
CHECKS:
├── Magic numbers: Will someone understand why this is 86400 (seconds/day)?
├── Implicit ordering: If someone reorders these lines, does it break?
├── Naming drift: Do the names still match if the behavior changes?
├── Interface fragility: Does adding a field to a struct break this?
├── Copy-paste traps: Is this code similar to nearby code that could diverge?
└── Delete safety: If someone removes the function this depends on, is the error clear?
```

## Review Output Format

```
╔══════════════════════════════════════════════════════════════╗
║                      REVIEW LENS                            ║
║           File: src/checkout/payment.ts                     ║
║           Lines changed: 47 (+32 / -15)                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  FINDINGS: 4 issues (1 critical, 1 high, 2 medium)          ║
║                                                              ║
║  🔴 CRITICAL [State Transition] Line 34-38                   ║
║  Payment charged before inventory reserved. If reservation   ║
║  fails, customer is charged for unfulfillable order.         ║
║  → Fix: Wrap in transaction. Reserve first, charge second.   ║
║                                                              ║
║  🟠 HIGH [Performance Cliff] Line 22                         ║
║  getOrderItems() inside loop = N+1 query pattern.            ║
║  Fine with test data (5 orders), catastrophic in production  ║
║  (5,000+ orders). Response time: O(n) DB calls.              ║
║  → Fix: Batch query with WHERE order_id IN (...).            ║
║                                                              ║
║  🟡 MEDIUM [Boundary] Line 15                                ║
║  `items.reduce()` on potentially empty array throws.         ║
║  → Fix: Add initialValue: items.reduce((a,b) => a+b, 0)     ║
║                                                              ║
║  🟡 MEDIUM [Implicit Assumption] Line 41                     ║
║  Assumes currency is always USD (hardcoded cents conversion). ║
║  → Fix: Use order.currency to determine decimal places.      ║
║                                                              ║
║  ✅ PASSED: Failure paths, security surface, change safety    ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- **Before every PR.** Run it on your own code before asking humans to review.
- During review of unfamiliar code (lenses help you know where to look)
- After writing any code that handles money, auth, or user data
- When reviewing code that "works in testing" before it hits production
- When you have a nagging feeling something is wrong but can't articulate what

## Why It Matters

Most code review catches 15-30% of defects. The defects that slip through aren't the obvious ones — they're the edge cases, the race conditions, the performance cliffs, and the implicit assumptions that only reveal themselves under production conditions.

Review Lens doesn't replace human reviewers. It catches what humans are systematically bad at seeing.

Zero external dependencies. Zero API calls. Pure structural and logical analysis.
