"""Lightweight data models using dataclasses — no Pydantic dependency."""
from dataclasses import dataclass, field, asdict
from typing import List, Optional
import json


@dataclass
class RawReference:
    """A reference extracted from a PDF before resolution."""
    raw_text: str
    title: Optional[str] = None
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Paper:
    id: str
    title: str
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    citation_count: int = 0
    abstract: Optional[str] = None
    url: Optional[str] = None
    is_seed: bool = False
    resolved: bool = True
    source: str = "semantic_scholar"
    doi: Optional[str] = None
    arxiv_id: Optional[str] = None
    pdf_url: Optional[str] = None
    refs_expanded: bool = False
    cites_expanded: bool = False

    def to_dict(self):
        return asdict(self)


@dataclass
class GraphData:
    nodes: List[Paper] = field(default_factory=list)
    edges: List[dict] = field(default_factory=list)
    seed_papers: List[str] = field(default_factory=list)
    depth: int = 1
    total_papers: int = 0

    def to_dict(self):
        return {
            "nodes": [n.to_dict() for n in self.nodes],
            "edges": self.edges,
            "seed_papers": self.seed_papers,
            "depth": self.depth,
            "total_papers": self.total_papers,
        }

    def save(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)

    @classmethod
    def load(cls, path: str) -> "GraphData":
        with open(path) as f:
            data = json.load(f)
        # Filter out unknown keys so older/newer JSON files load gracefully
        paper_fields = {f.name for f in Paper.__dataclass_fields__.values()}
        nodes = []
        for n in data.get("nodes", []):
            filtered = {k: v for k, v in n.items() if k in paper_fields}
            nodes.append(Paper(**filtered))
        return cls(
            nodes=nodes,
            edges=data.get("edges", []),
            seed_papers=data.get("seed_papers", []),
            depth=data.get("depth", 1),
            total_papers=data.get("total_papers", len(nodes)),
        )

    # --- Helper methods for graph mutations ---

    def node_ids(self) -> set:
        return {n.id for n in self.nodes}

    def edge_keys(self) -> set:
        return {(e["source"], e["target"]) for e in self.edges}

    def find_node(self, node_id: str) -> Optional[Paper]:
        for n in self.nodes:
            if n.id == node_id:
                return n
        return None

    def add_node(self, paper: Paper) -> bool:
        """Add node if not duplicate. If exists, upgrade metadata/seed status.
        Returns True if a new node was added."""
        existing = self.find_node(paper.id)
        if existing is not None:
            # Upgrade seed status (one-way: non-seed -> seed)
            if paper.is_seed and not existing.is_seed:
                existing.is_seed = True
                if paper.id not in self.seed_papers:
                    self.seed_papers.append(paper.id)
            # Fill in missing metadata
            if not existing.abstract and paper.abstract:
                existing.abstract = paper.abstract
            if not existing.doi and paper.doi:
                existing.doi = paper.doi
            if not existing.arxiv_id and paper.arxiv_id:
                existing.arxiv_id = paper.arxiv_id
            if not existing.url and paper.url:
                existing.url = paper.url
            if not existing.pdf_url and paper.pdf_url:
                existing.pdf_url = paper.pdf_url
            if paper.citation_count > existing.citation_count:
                existing.citation_count = paper.citation_count
            if paper.refs_expanded:
                existing.refs_expanded = True
            if paper.cites_expanded:
                existing.cites_expanded = True
            return False
        self.nodes.append(paper)
        if paper.is_seed and paper.id not in self.seed_papers:
            self.seed_papers.append(paper.id)
        self.total_papers = len(self.nodes)
        return True

    def add_edge(self, source: str, target: str, edge_type: str = "cites") -> bool:
        """Add edge if not duplicate. Returns True if added."""
        key = (source, target)
        if key in self.edge_keys():
            return False
        self.edges.append({"source": source, "target": target, "type": edge_type})
        return True

    def remove_seed(self, seed_id: str) -> dict:
        """Remove a seed paper and its exclusive connections.
        Returns stats about what was removed."""
        if seed_id not in self.seed_papers:
            return {"removed_nodes": 0, "removed_edges": 0}

        # Find connected nodes
        connected = set()
        for e in self.edges:
            if e["source"] == seed_id:
                connected.add(e["target"])
            if e["target"] == seed_id:
                connected.add(e["source"])

        # Find exclusive nodes (not connected to any other seed)
        other_seeds = [s for s in self.seed_papers if s != seed_id]
        exclusive = set()
        for nid in connected:
            if nid in self.seed_papers:
                continue
            is_exclusive = True
            for e in self.edges:
                if (e["source"] == nid and e["target"] in other_seeds) or \
                   (e["target"] == nid and e["source"] in other_seeds):
                    is_exclusive = False
                    break
            if is_exclusive:
                exclusive.add(nid)

        to_remove = {seed_id} | exclusive
        old_edge_count = len(self.edges)
        self.nodes = [n for n in self.nodes if n.id not in to_remove]
        self.edges = [e for e in self.edges
                      if e["source"] not in to_remove and e["target"] not in to_remove]
        self.seed_papers = [s for s in self.seed_papers if s != seed_id]
        self.total_papers = len(self.nodes)

        return {
            "removed_nodes": len(to_remove),
            "removed_edges": old_edge_count - len(self.edges),
        }

    def remove_node(self, node_id: str) -> dict:
        """Remove a single non-seed node and its incident edges."""
        if node_id in self.seed_papers:
            return {"error": "Cannot remove seed paper with remove_node. Use remove_seed()."}
        node = self.find_node(node_id)
        if not node:
            return {"removed_nodes": 0, "removed_edges": 0}
        before_edges = len(self.edges)
        self.nodes = [n for n in self.nodes if n.id != node_id]
        self.edges = [e for e in self.edges
                      if e["source"] != node_id and e["target"] != node_id]
        self.total_papers = len(self.nodes)
        return {
            "removed_nodes": 1,
            "removed_edges": before_edges - len(self.edges),
        }


@dataclass
class SearchResult:
    total: int
    papers: List[Paper]

    def to_dict(self):
        return {"total": self.total, "papers": [p.to_dict() for p in self.papers]}
