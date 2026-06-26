---
name: transitive_closure_generator
title: Transitive Closure Generator
description: Compute transitive closure on graphs to infer implicit relationships and expand graphs with logically implied connections. Supports multiple algorithms and cycle detection for dependency analysis, hierarchies, and reachability.
category: reasoning
tags:
  - knowledge-graph
  - reasoning
  - inference
  - transitive-closure
  - graph-algorithms
  - dependency-analysis
  - reachability
  - hierarchy
  - path-materialization
  - graph-expansion
version: 1.0.0
author: community
license: MIT
metadata:
  {"openclaw":{"emoji":"🔀","homepage":"https://clawhub.com"}}
---

# Transitive Closure Generator

**Compute transitive closure on graphs to automatically infer implicit relationships and expand knowledge graphs.**

This skill computes the transitive closure of relations, deriving all logically implied connections from existing relationships and materializing them as explicit edges.

## Quick Start

### Use When
- Computing ancestor relationships from parent chains
- Inferring dependency chains in software
- Expanding hierarchical relationships
- Finding reachability in networks
- Materializing transitive relations
- Analyzing organizational hierarchies
- Building complete dependency graphs
- Expanding knowledge graph completeness

### Inputs
- Graph edges (relationship pairs)
- Relation type to compute closure for
- Optional: Maximum depth/hops
- Optional: Cycle detection and handling

### Outputs
- Transitive closure edges (all reachable pairs)
- Path information (distances, intermediates)
- Reachability analysis
- Cycle detection results
- Statistics and metrics

## Transitive Closure Concepts

### Transitive Relation
A relation where if A→B and B→C then A→C.

Examples:
```
ancestor_of:      A ancestor_of B ∧ B ancestor_of C ⇒ A ancestor_of C
depends_on:       A depends B ∧ B depends C ⇒ A depends C
located_in:       Paris located_in France ∧ France located_in Europe ⇒ Paris located_in Europe
subclass_of:      Dog subclass_of Mammal ∧ Mammal subclass_of Animal ⇒ Dog subclass_of Animal
```

### Non-Transitive Relations
Relations where transitivity doesn't apply:
```
friend_of:        A friend B ∧ B friend C ⇏ A friend C (not necessarily)
married_to:       A married B ∧ B married C ⇏ A married C (false)
knows:            A knows B ∧ B knows C ⇏ A knows C (uncertain)
```

### Transitive Closure Set
The complete set of all pairs (a,b) where a can reach b.

Example:
```
Original edges:
  A → B
  B → C
  C → D

Transitive closure:
  Direct:   A→B, B→C, C→D (3 edges)
  Inferred: A→C, A→D, B→D (3 additional edges)
  Total:    6 edges
```

### Path Materialization
Converting implicit paths into explicit edges.

```
Implicit chain: A ---> B ---> C ---> D
Materialized:   A → C (2 hops), A → D (3 hops), etc.
```

### Reachability
Set of all nodes reachable from a given node.

```
From A: {B, C, D}
From B: {C, D}
From C: {D}
```

## Closure Computation Algorithms

### Algorithm 1: Depth-First Search (DFS)

Find all reachable nodes from each source node.

**Complexity:** O(V * (V + E))  
**Space:** O(V)  
**Best For:** Small to medium graphs

```
For each node N:
  Visited = {}
  DFS(N, Visited)
  Add all visited nodes as reachable
```

---

### Algorithm 2: Breadth-First Search (BFS)

Level-by-level traversal to find all reachable nodes.

**Complexity:** O(V * (V + E))  
**Space:** O(V)  
**Best For:** Finding shortest paths, layered structures

```
For each node N:
  Queue = {N}
  While Queue not empty:
    Current = Queue.pop()
    For each neighbor of Current:
      If not visited:
        Mark visited
        Add to closure
        Queue.push(neighbor)
```

---

### Algorithm 3: Floyd-Warshall

Compute all-pairs shortest paths and closure simultaneously.

**Complexity:** O(V³)  
**Space:** O(V²)  
**Best For:** Dense graphs, need all distances

```
D[i][j] = direct edge weight or ∞
For each intermediate k:
  For each pair (i,j):
    D[i][j] = min(D[i][j], D[i][k] + D[k][j])
    If D[i][j] < ∞, add to closure
```

---

### Algorithm 4: Warshall's Algorithm

Specialized for transitive closure computation.

**Complexity:** O(V³)  
**Space:** O(V²)  
**Best For:** Dense graphs, pure closure (no distances)

```
TC[i][j] = 1 if edge exists, 0 otherwise
For each k in 0..V:
  For each i in 0..V:
    For each j in 0..V:
      TC[i][j] = TC[i][j] OR (TC[i][k] AND TC[k][j])
```

---

### Algorithm 5: Incremental Closure

Update closure incrementally when edges are added.

**Complexity:** O(added_edges * V)  
**Space:** O(V²)  
**Best For:** Dynamic graphs, continuous updates

```
On add edge (u, v):
  Mark TC[u][v] = 1
  For all (i,u) and (v,j) in TC:
    Mark TC[i][j] = 1
  Propagate transitively
```

---

## Cycle Detection

### DAG Assumption
Most transitive closure algorithms assume acyclic graphs (DAGs).

Cycles cause:
- Infinite expansion
- Incorrect closure results
- Performance issues

### Detection Methods

#### Method 1: Color-Based DFS
```
Colors: White (unvisited), Gray (visiting), Black (done)
If reach Gray node: cycle detected
```

#### Method 2: Topological Sort
```
If can't perform complete topological sort: contains cycle
```

#### Method 3: Negative Weight Cycles (Bellman-Ford)
```
If shortest path becomes negative: cycle in weight sense
```

---

## Materialization Strategies

### Full Materialization
Store all closure edges explicitly.

```
Pros: O(1) query, no computation needed
Cons: Storage overhead O(V²), update cost
```

### Lazy Computation
Compute paths on-demand.

```
Pros: No storage overhead
Cons: Query time O(V+E), repeated computation
```

### Hybrid Approach
Materialize high-value closures, compute others on-demand.

```
Pros: Balanced cost/benefit
Cons: Complexity
```

---

## Performance Optimization

### Optimization 1: Memoization

Cache computed reachability sets.

```python
reachable_cache = {}
def get_reachable(node):
    if node in reachable_cache:
        return reachable_cache[node]
    result = compute_reachable_bfs(node)
    reachable_cache[node] = result
    return result
```

---

### Optimization 2: Incremental Updates

Update only affected paths when new edges added.

```
New edge (u, v):
  - Find all nodes that can reach u
  - Find all nodes reachable from v
  - Add edges from reaching→v reachable
```

---

### Optimization 3: Bidirectional Search

Search from both source and target.

```
Forward reach from source
Backward reach to target
Intersection = connected pairs
```

---

## Error Handling

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Infinite loop | Cycles in graph | Detect and handle cycles |
| Memory overflow | Too many inferred edges | Lazy materialization, sampling |
| Performance timeout | O(V³) on large graph | Use faster algorithm, incremental |
| Incorrect results | Assuming non-transitive as transitive | Validate relation type |
| Duplicate edges | Not deduplicating | Track seen edges |

---

## Best Practices

✓ **Verify transitivity** - Ensure relation is truly transitive  
✓ **Detect cycles early** - Prevent infinite loops  
✓ **Choose right algorithm** - Match to graph size and density  
✓ **Use memoization** - Cache frequently computed paths  
✓ **Handle large graphs** - Consider lazy evaluation  
✓ **Monitor performance** - Track closure computation time  
✓ **Validate results** - Check for correctness  
✓ **Consider updates** - Plan for incremental changes  
✓ **Document assumptions** - Clarify which relations are transitive  
✓ **Test with sample data** - Verify on small graphs first  

## Advanced Features

### Weighted Transitive Closure
Compute closure with edge weights (e.g., confidence, cost).

### Probabilistic Closure
Handle uncertain relationships with confidence scores.

### Temporal Closure
Time-aware transitive closure considering timestamps.

### Approximate Closure
Fast approximation for large graphs.

### Cross-Graph Closure
Compute closure across multiple interconnected graphs.

## Integration Points

This skill integrates with:

- **Graph Rule Engine Builder** - Define transitive rules
- **Ontology-Based Inference** - Compute ontology closure
- **Causal Chain Analyzer** - Analyze causal chains
- **Graph Path Reasoning Analyzer** - Find reachable paths
- **Multi-Hop Reasoning Query Builder** - Build queries

## Recommended Libraries

### Graph Algorithms
- `networkx` - DFS, BFS, topological sort
- `scipy.sparse` - Sparse matrix operations
- `numpy` - Matrix operations for Warshall

### Optimization
- `functools.lru_cache` - Memoization
- `collections.deque` - Queue for BFS

### Analysis
- `igraph` - Fast graph algorithms
- `graph-tool` - High-performance analysis

## Related Skills

- **Graph Rule Engine Builder** - Define transitive rules
- **Ontology-Based Inference** - Class hierarchy closure
- **Causal Chain Analyzer** - Analyze causal paths
- **Graph Path Reasoning Analyzer** - Find all paths
- **Multi-Hop Reasoning Query Builder** - Complex queries

---

**Version:** 1.0.0
