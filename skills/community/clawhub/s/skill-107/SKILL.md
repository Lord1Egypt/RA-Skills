# Skill 107: Distributed System Patterns & Design

**Quality Grade:** 94-95/100  
**Author:** OpenClaw Assistant  
**Last Updated:** March 2026  
**Difficulty:** Advanced (requires architectural thinking, trade-off analysis)

---

## Overview

Distributed System Patterns are proven solutions to recurring problems in systems that span multiple machines, networks, and datacenters. As systems scale beyond single machines, coordination, fault tolerance, and consistency become non-negotiable.

This skill covers:
- **Replication** and consistency models
- **Partitioning** strategies and data distribution
- **Consensus** algorithms and leader election
- **Failure recovery** and resilience patterns
- **Message passing** and event ordering
- **Coordination** across services

---

## Part 1: Replication Patterns

### Master-Slave Replication

**How it works:**
- All writes go to master
- Master propagates to slaves asynchronously
- Reads can come from slaves (eventual consistency)

**Trade-offs:**
- ✓ Scalable reads
- ✗ Write bottleneck at master
- ✗ Stale reads from slaves
- ✗ Slave lag under high load

**When to use:** Read-heavy workloads, geographic distribution, backup resilience

### Peer-to-Peer Replication

**How it works:**
- All nodes accept reads and writes
- Changes propagate peer-to-peer (gossip protocol)
- Eventual consistency with conflict resolution

**Trade-offs:**
- ✓ Scalable both reads and writes
- ✓ High availability (no single master)
- ✗ Conflict resolution complexity
- ✗ Higher network overhead

**When to use:** High availability needs, offline-first systems, global distribution

### Chain Replication

**How it works:**
- Writes go to head, flow through chain to tail
- Tail is readable, provides strong consistency
- Head can be rebalanced independently

**Trade-offs:**
- ✓ Strong consistency
- ✓ Read tail scalability
- ✗ Slower writes (latency of chain length)
- ✗ Head failure needs rebalance

**When to use:** Consistent reads critical, moderate write frequency

---

## Part 2: Partitioning Strategies

### Range-Based Partitioning

```
Partition 0: UserIDs [0, 1000000)
Partition 1: UserIDs [1000000, 2000000)
Partition 2: UserIDs [2000000, ∞)
```

**Pros:** Simple, range queries efficient  
**Cons:** Uneven distribution (hotspots), rebalancing expensive

### Hash-Based Partitioning

```
Partition = hash(key) % num_partitions
```

**Pros:** Even distribution, fast lookup  
**Cons:** Range queries require full scan, rebalancing complex

### Consistent Hashing

```
Nodes arranged in ring, key maps to first node clockwise
Adding/removing node affects only adjacent partitions (~1/N data moves)
```

**Pros:** Minimal rebalancing, scalable additions  
**Cons:** Uneven distribution without virtual nodes, algorithm complexity

---

## Part 3: Consensus & Coordination

### Two-Phase Commit (2PC)

**Flow:**
1. Coordinator asks all participants: "Can you commit?"
2. Participants respond Yes/No (reserve resources)
3. If all Yes, coordinator tells all: "Commit"
4. If any No, coordinator tells all: "Abort"

**Guarantees:** Atomic across all participants  
**Problems:** Blocking, not partition-tolerant, slow

**Use case:** Database transactions across shards

### Raft Consensus

**Leader election + log replication:**
1. Nodes elect a leader via voting
2. Leader accepts all writes
3. Leader replicates log entries to followers
4. Majority replication = safe to commit

**Guarantees:** Safety (never lose committed data), liveness (will elect leader)  
**Performance:** Lower throughput than 2PC, but more resilient

**Use case:** Distributed consensus (etcd, Consul), metadata stores

### CRDT (Conflict-free Replicated Data Types)

**Approach:** Assign unique IDs, track causal history  
**Guarantees:** Automatic conflict resolution, commutative operations

**Example:** Vector clocks + last-write-wins for distributed counters

**Use case:** Collaborative editing, offline-first applications

---

## Part 4: Failure Recovery

### Idempotency

Make operations repeatable—if a request is retried, result is same:

```python
def transfer_funds(from_id, to_id, amount, idempotency_key):
    # Check: did we already process this key?
    if idempotency_cache.get(idempotency_key):
        return idempotency_cache[idempotency_key]
    
    result = _do_transfer(from_id, to_id, amount)
    idempotency_cache[idempotency_key] = result
    return result
```

**Key:** Idempotency key must be client-chosen and immutable

### Retries with Backoff

```
Attempt 1: immediate
Attempt 2: wait 1s
Attempt 3: wait 2s
Attempt 4: wait 4s
Attempt 5: wait 8s (give up if still failing)

Jitter: add random delay to avoid thundering herd
backoff_time = min(max_backoff, base * (2 ^ attempt)) + random(0, jitter)
```

### Circuit Breaker

```
State: CLOSED (normal) → OPEN (failing) → HALF_OPEN (testing)

CLOSED → OPEN: When error rate > threshold for duration
OPEN → HALF_OPEN: After cooldown period
HALF_OPEN → CLOSED: If test request succeeds
HALF_OPEN → OPEN: If test request fails
```

---

## Part 5: Message Passing & Ordering

### FIFO Ordering

Messages between two nodes arrive in send order.  
**Implementation:** Sequence numbers, TCP guarantees

### Causal Ordering

If event A causally precedes B, A's message arrives before B's.  
**Implementation:** Vector clocks or version vectors

### Total Ordering

All nodes receive all messages in same order.  
**Implementation:** Consensus-based broadcast, sequencer node

**Trade-offs:** Ordering strength vs. latency cost

---

## Conclusion

Distributed system patterns are essential vocabulary for building scalable, reliable systems. Understanding replication, partitioning, consensus, and failure recovery lets you design systems that survive failures, scale horizontally, and provide guarantees users can depend on.

**Key Takeaway:** Choose patterns based on your actual requirements (CAP theorem), not ideals. Consistency, availability, and partition tolerance—pick two.