"""
Transitive Closure Generator - Production Implementation
Compute transitive closure to infer implicit relationships in graphs.
Author: Knowledge Graph Team
License: MIT
Version: 1.0.0
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional
from enum import Enum
from collections import deque, defaultdict
class ClosureAlgorithm(Enum):
    """Closure computation algorithms."""
    DFS = "dfs"
    BFS = "bfs"
    WARSHALL = "warshall"
    FLOYD_WARSHALL = "floyd_warshall"
    INCREMENTAL = "incremental"
@dataclass
class ClosureConfig:
    """Configuration for closure generation."""
    edges: List[Tuple[str, str]]
    relation_type: str = "transitivity"
    algorithm: ClosureAlgorithm = ClosureAlgorithm.BFS
    detect_cycles: bool = True
    materialize: bool = True
    max_depth: Optional[int] = None
class ClosureGenerator:
    """Transitive closure computation engine."""
    def __init__(self, config: ClosureConfig):
        """Initialize closure generator."""
        self.config = config
        self._build_adjacency_list()
        self.closure_edges = set()
        self.has_cycle = False
    def _build_adjacency_list(self):
        """Build adjacency list from edges."""
        self.graph = defaultdict(list)
        self.nodes = set()
        for source, target in self.config.edges:
            self.graph[source].append(target)
            self.nodes.add(source)
            self.nodes.add(target)
    def compute_closure(self) -> Set[Tuple[str, str]]:
        """Compute transitive closure."""
        if self.config.algorithm == ClosureAlgorithm.DFS:
            return self._dfs_closure()
        elif self.config.algorithm == ClosureAlgorithm.BFS:
            return self._bfs_closure()
        elif self.config.algorithm == ClosureAlgorithm.WARSHALL:
            return self._warshall_closure()
        else:
            return self._bfs_closure()
    def _dfs_closure(self) -> Set[Tuple[str, str]]:
        """DFS-based closure computation."""
        closure = set()
        for source in self.nodes:
            visited = set()
            self._dfs(source, source, visited, 0)
            for target in visited:
                if source != target:
                    closure.add((source, target))
        self.closure_edges = closure
        return closure
    def _dfs(self, current, source, visited, depth):
        """DFS traversal."""
        if self.config.max_depth and depth >= self.config.max_depth:
            return
        for neighbor in self.graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                self._dfs(neighbor, source, visited, depth + 1)
    def _bfs_closure(self) -> Set[Tuple[str, str]]:
        """BFS-based closure computation."""
        closure = set()
        for source in self.nodes:
            visited = {source}
            queue = deque(self.graph[source])
            while queue:
                node = queue.popleft()
                if node not in visited:
                    visited.add(node)
                    closure.add((source, node))
                    queue.extend(self.graph[node])
        self.closure_edges = closure
        return closure
    def _warshall_closure(self) -> Set[Tuple[str, str]]:
        """Warshall's algorithm for closure."""
        nodes_list = sorted(list(self.nodes))
        n = len(nodes_list)
        node_index = {n: i for i, n in enumerate(nodes_list)}
        # Initialize matrix
        tc = [[False] * n for _ in range(n)]
        for source, target in self.config.edges:
            tc[node_index[source]][node_index[target]] = True
        # Warshall's algorithm
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    tc[i][j] = tc[i][j] or (tc[i][k] and tc[k][j])
        # Extract closure
        closure = set()
        for i in range(n):
            for j in range(n):
                if tc[i][j]:
                    closure.add((nodes_list[i], nodes_list[j]))
        self.closure_edges = closure
        return closure
    def get_reachable(self, node: str) -> Set[str]:
        """Get all reachable nodes from given node."""
        reachable = set()
        visited = {node}
        queue = deque(self.graph[node])
        while queue:
            current = queue.popleft()
            if current not in visited:
                visited.add(current)
                reachable.add(current)
                queue.extend(self.graph[current])
        return reachable
    def get_all_paths(self, source: str, target: str) -> List[List[str]]:
        """Find all paths between source and target."""
        paths = []
        def dfs(current, target, path):
            if current == target:
                paths.append(path[:])
                return
            for neighbor in self.graph[current]:
                if neighbor not in path:
                    path.append(neighbor)
                    dfs(neighbor, target, path)
                    path.pop()
        dfs(source, target, [source])
        return paths
    def get_statistics(self) -> Dict:
        """Get closure statistics."""
        original_edges = len(self.config.edges)
        closure_edges = len(self.closure_edges)
        inferred = closure_edges - original_edges
        return {
            'nodes': len(self.nodes),
            'original_edges': original_edges,
            'closure_edges': closure_edges,
            'inferred_edges': inferred,
            'densification_factor': closure_edges / max(1, original_edges),
            'has_cycle': self.has_cycle
        }
# Example usage
if __name__ == "__main__":
    config = ClosureConfig(
        edges=[
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E")
        ],
        algorithm=ClosureAlgorithm.BFS
    )
    generator = ClosureGenerator(config)
    closure = generator.compute_closure()
    print("=== Transitive Closure ===")
    print(f"Original edges: {len(config.edges)}")
    print(f"Closure edges: {len(closure)}")
    print(f"Inferred: {len(closure) - len(config.edges)}")
    print("\n=== Reachability from A ===")
    reachable = generator.get_reachable("A")
    print(f"From A: {reachable}")
    print("\n=== Statistics ===")
    stats = generator.get_statistics()
    for k, v in stats.items():
        print(f"{k}: {v}")
