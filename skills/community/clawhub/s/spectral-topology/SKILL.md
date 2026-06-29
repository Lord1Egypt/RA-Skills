# Spectral Topology Engine — Skill

## Overview
Detect structural holes, hidden dependencies, and missing links in directed networks using eigenvalue decomposition of a combined adjacency + similarity matrix.

## Location
`/home/openclaw/.openclaw/workspace/topology-engine/topology_engine.py`

## Quick Usage

```python
from topology_engine import GraphBuilder, SpectralTopologyAnalyzer, quick_analyze

# From edge list: (source, target, weight)
report = quick_analyze([(0,1,1.0), (1,2,1.0), (2,0,1.0)], n_nodes=3, alpha=0.3)
print(report.summary())

# With metadata similarity
features = np.array([[1,0], [0.9,0.1], [0,1]])
sim = GraphBuilder.cosine_similarity_matrix(features)
adj = GraphBuilder.from_edge_list(3, [(0,1,1.0), (1,2,1.0)])
analyzer = SpectralTopologyAnalyzer(alpha=0.3)
report = analyzer.analyze(adj, similarity=sim)
```

## Key Concepts
- **Negative eigenvalues** = structural gaps (edges that should exist but don't)
- **Alpha** = weighting for metadata similarity vs explicit graph structure (default 0.3)
- **Spectral gap** = difference between largest eigenvalues (measures overall connectivity)
- **Cohesion vectors** = identify which nodes participate in each gap

## Output
- `TopologyReport` with `.summary()` for human-readable output
- `.to_json(path)` for export
- `.gaps` list of `StructuralGap` objects with eigenvalue, node_indices, node_weights
