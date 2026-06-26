# Transitive Closure Algorithms & Patterns
## Algorithm 1: DFS-Based Closure
```python
def dfs_closure(graph):
    closure = set()
    for node in graph.nodes():
        visited = set()
        dfs(node, node, visited)
        for target in visited:
            if target != node:
                closure.add((node, target))
    return closure
```
Complexity: O(V*(V+E)), Space: O(V), Best for: Small graphs
## Algorithm 2: BFS-Based Closure
```python
def bfs_closure(graph):
    closure = set()
    for source in graph.nodes():
        visited = {source}
        queue = deque(graph[source])
        while queue:
            node = queue.popleft()
            if node not in visited:
                visited.add(node)
                closure.add((source, node))
                queue.extend(graph[node])
    return closure
```
Complexity: O(V*(V+E)), Space: O(V), Best for: Level-based traversal
## Algorithm 3: Warshall's Algorithm
```
TC[i][j] = 1 if edge, 0 else
For k in V:
    For i in V:
        For j in V:
            TC[i][j] = TC[i][j] OR (TC[i][k] AND TC[k][j])
```
Complexity: O(V³), Space: O(V²), Best for: Dense graphs
## Algorithm 4: Floyd-Warshall
Similar to Warshall but also computes shortest distances.
Complexity: O(V³), Can track paths
## Algorithm 5: Incremental Closure
Update closure when edges added:
```
On add (u,v):
  TC[u][v] = 1
  For all (i,u) and (v,j):
    TC[i][j] = 1
```
Complexity: O(V) per edge, Best for: Dynamic graphs
## Cycle Detection (DFS coloring)
Colors: WHITE, GRAY, BLACK
If reach GRAY node → cycle detected
## Memoization Pattern
```python
@functools.lru_cache(maxsize=None)
def get_reachable(node):
    return compute_reachable_bfs(node)
```
## Materialization Strategies
1. Full: Store all closure edges (fast query, high storage)
2. Lazy: Compute on-demand (low storage, slow query)
3. Hybrid: Materialize common, compute rare
---
**Summary:**
- Use DFS/BFS for sparse graphs
- Use Warshall for dense graphs
- Incremental for dynamic graphs
- Cache for repeated queries
