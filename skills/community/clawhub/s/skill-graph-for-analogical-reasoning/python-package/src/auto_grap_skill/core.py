from __future__ import annotations

import json
import math
import os
import platform
import re
import shutil
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml


TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_+-]{1,}")
CODE_REF_RE = re.compile(r"`([^`]+)`")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)
TRIGGER_HINTS = (
    "use this when",
    "use this skill when",
    "when users request",
    "when the user asks",
    "trigger conditions",
    "for tasks like",
    "works best when",
)
STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "when",
    "your",
    "into",
    "then",
    "than",
    "they",
    "them",
    "their",
    "have",
    "will",
    "while",
    "what",
    "where",
    "which",
    "using",
    "used",
    "user",
    "users",
    "skill",
    "skills",
    "agent",
    "claude",
    "should",
    "through",
    "about",
    "only",
    "more",
    "just",
    "into",
    "each",
    "like",
    "than",
    "also",
    "does",
    "need",
    "needs",
    "must",
    "guide",
}
ACTION_HINTS = {
    "create",
    "write",
    "build",
    "design",
    "review",
    "summarize",
    "extract",
    "test",
    "analyze",
    "edit",
    "generate",
    "debug",
    "fill",
    "convert",
    "process",
    "draft",
}
TOOL_NOISE = {
    "add",
    "all",
    "bash",
    "build",
    "check",
    "command",
    "content",
    "convert",
    "create",
    "dataframe",
    "document",
    "extract",
    "file",
    "files",
    "form",
    "forms",
    "hello",
    "html",
    "if",
    "image",
    "images",
    "import",
    "input",
    "json",
    "line",
    "merge",
    "metadata",
    "normal",
    "open",
    "output",
    "page",
    "pages",
    "path",
    "pdf",
    "print",
    "python",
    "read",
    "reference",
    "report",
    "requires",
    "row",
    "save",
    "split",
    "story",
    "styles",
    "table",
    "tables",
    "task",
    "tasks",
    "text",
    "title",
    "tool",
    "tools",
    "true",
    "write",
    "writer",
    "above",
    "access",
    "actually",
    "active",
    "added",
    "adding",
    "additional",
    "adjust",
    "after",
    "again",
    "alignment",
    "always",
    "analysis",
    "analyze",
    "any",
    "api",
    "are",
    "automatically",
    "avoid",
    "able",
    "across",
}


@dataclass
class SkillNode:
    id: str
    name: str
    description: str
    version: str | None
    source_dir: str
    source_file: str
    headings: list[str]
    triggers: list[str]
    body_excerpt: str
    tool_mentions: list[str]
    requires_env: list[str]
    requires_bins: list[str]
    os_restrictions: list[str]
    tokens: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    tfidf: dict[str, float] = field(default_factory=dict)
    desc_tfidf: dict[str, float] = field(default_factory=dict)
    trigger_tfidf: dict[str, float] = field(default_factory=dict)


@dataclass
class SkillEdge:
    source: str
    target: str
    weight: float
    dominant_relation: str
    relation_scores: dict[str, float]
    view_weights: dict[str, float] = field(default_factory=dict)
    evidence: list[str] = field(default_factory=list)


def tokenize(text: str) -> list[str]:
    lowered = text.lower().replace("/", " ").replace("-", " ").replace(".", " ")
    return [token for token in TOKEN_RE.findall(lowered) if token not in STOPWORDS]


def normalize_id(name: str, fallback: str) -> str:
    base = (name or fallback).strip().lower().replace(" ", "-").replace("_", "-")
    base = re.sub(r"[^a-z0-9-]+", "-", base)
    base = re.sub(r"-+", "-", base).strip("-")
    return base or fallback


def cosine_similarity(left: dict[str, float], right: dict[str, float]) -> float:
    if not left or not right:
        return 0.0
    common = set(left) & set(right)
    dot = sum(left[key] * right[key] for key in common)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0
    return dot / (left_norm * right_norm)


def jaccard_similarity(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def overlap_fraction(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left)


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def extract_code_refs(body: str) -> list[str]:
    refs: set[str] = set()
    for match in CODE_REF_RE.findall(body):
        for token in tokenize(match):
            if (
                token.isdigit()
                or token in TOOL_NOISE
                or len(token) < 3
                or not re.fullmatch(r"[a-z][a-z0-9_-]*", token)
                or re.search(r"\d", token)
            ):
                continue
            refs.add(token)
    return sorted(refs)


def split_frontmatter(raw: str) -> tuple[dict[str, Any], str]:
    match = FRONTMATTER_RE.match(raw)
    if not match:
        return {}, raw
    frontmatter_text, body = match.groups()
    parsed = yaml.safe_load(frontmatter_text) or {}
    if not isinstance(parsed, dict):
        return {}, body
    return parsed, body


def extract_headings(body: str) -> list[str]:
    return [
        line.lstrip("#").strip()
        for line in body.splitlines()
        if line.strip().startswith("#")
    ]


def extract_trigger_lines(body: str) -> list[str]:
    lines = [line.strip("- ").strip() for line in body.splitlines() if line.strip()]
    results: list[str] = []
    for line in lines:
        lowered = line.lower()
        if any(hint in lowered for hint in TRIGGER_HINTS):
            results.append(line)
    return results[:20]


def top_keywords(tokens: list[str], *, limit: int = 12) -> list[str]:
    counts = Counter(tokens)
    ordered = sorted(counts.items(), key=lambda item: (-item[1], item[0]))
    return [token for token, _ in ordered[:limit]]


def compute_tfidf(corpus_tokens: list[list[str]]) -> tuple[list[dict[str, float]], dict[str, float]]:
    doc_count = len(corpus_tokens)
    doc_freq: Counter[str] = Counter()
    for tokens in corpus_tokens:
        doc_freq.update(set(tokens))

    idf = {
        token: math.log((1 + doc_count) / (1 + freq)) + 1.0
        for token, freq in doc_freq.items()
    }

    vectors: list[dict[str, float]] = []
    for tokens in corpus_tokens:
        tf = Counter(tokens)
        length = max(len(tokens), 1)
        vector = {
            token: (count / length) * idf[token]
            for token, count in tf.items()
            if token in idf
        }
        vectors.append(vector)
    return vectors, idf


def normalized_tf(tokens: list[str]) -> dict[str, float]:
    counts = Counter(tokens)
    length = max(len(tokens), 1)
    return {token: count / length for token, count in counts.items()}


def flatten_text(frontmatter: dict[str, Any], body: str) -> str:
    description = str(frontmatter.get("description") or "")
    name = str(frontmatter.get("name") or "")
    headings = " ".join(extract_headings(body))
    triggers = " ".join(extract_trigger_lines(body))
    return "\n".join(part for part in (name, description, triggers, headings, body) if part)


def extract_openclaw_metadata(frontmatter: dict[str, Any]) -> tuple[list[str], list[str], list[str]]:
    metadata = frontmatter.get("metadata") or {}
    runtime = {}
    if isinstance(metadata, dict):
        runtime = (
            metadata.get("openclaw")
            or metadata.get("clawdbot")
            or metadata.get("clawdis")
            or {}
        )
    if not isinstance(runtime, dict):
        runtime = {}
    requires = runtime.get("requires") or {}
    if not isinstance(requires, dict):
        requires = {}
    requires_env = [str(item) for item in requires.get("env") or [] if item]
    requires_bins = [str(item) for item in requires.get("bins") or [] if item]
    os_restrictions = [str(item) for item in runtime.get("os") or [] if item]
    return requires_env, requires_bins, os_restrictions


def body_excerpt(body: str, *, limit: int = 400) -> str:
    text = re.sub(r"\s+", " ", body).strip()
    return text[:limit]


def build_readiness(node: SkillNode) -> tuple[float, list[str]]:
    evidence: list[str] = []
    current_os = platform.system().lower()
    os_map = {"darwin": "macos", "linux": "linux", "windows": "windows"}
    normalized_os = os_map.get(current_os, current_os)
    if node.os_restrictions and normalized_os not in {item.lower() for item in node.os_restrictions}:
        return 0.0, [f"os mismatch: requires {node.os_restrictions}"]

    missing_env = [env for env in node.requires_env if not os.getenv(env)]
    missing_bins = [binary for binary in node.requires_bins if not shutil.which(binary)]
    if missing_env:
        evidence.append(f"missing env: {', '.join(missing_env)}")
    if missing_bins:
        evidence.append(f"missing bins: {', '.join(missing_bins)}")
    if missing_env or missing_bins:
        return 0.4, evidence
    return 1.0, ["runtime ready"]


class GraphSkillEngine:
    def __init__(self, nodes: list[SkillNode], edges: list[SkillEdge], graph_path: Path | None = None):
        self.nodes = nodes
        self.edges = edges
        self.graph_path = graph_path
        self.nodes_by_id = {node.id: node for node in nodes}
        self.adjacency: dict[str, list[SkillEdge]] = {}
        for edge in edges:
            self.adjacency.setdefault(edge.source, []).append(edge)
            self.adjacency.setdefault(edge.target, []).append(edge)

    @classmethod
    def build_from_sources(cls, sources: list[Path]) -> "GraphSkillEngine":
        node_candidates = []
        for source in sources:
            node_candidates.extend(cls._discover_skills(source))

        if not node_candidates:
            raise ValueError("No skills with SKILL.md were found in the provided sources.")

        corpus = [node["full_text_tokens"] for node in node_candidates]
        corpus_vectors, _idf = compute_tfidf(corpus)
        desc_vectors, _ = compute_tfidf([node["description_tokens"] for node in node_candidates])
        trigger_vectors, _ = compute_tfidf([node["trigger_tokens"] for node in node_candidates])

        nodes: list[SkillNode] = []
        for index, candidate in enumerate(node_candidates):
            nodes.append(
                SkillNode(
                    id=candidate["id"],
                    name=candidate["name"],
                    description=candidate["description"],
                    version=candidate["version"],
                    source_dir=candidate["source_dir"],
                    source_file=candidate["source_file"],
                    headings=candidate["headings"],
                    triggers=candidate["triggers"],
                    body_excerpt=candidate["body_excerpt"],
                    tool_mentions=candidate["tool_mentions"],
                    requires_env=candidate["requires_env"],
                    requires_bins=candidate["requires_bins"],
                    os_restrictions=candidate["os_restrictions"],
                    tokens=candidate["full_text_tokens"],
                    keywords=top_keywords(candidate["keyword_tokens"]),
                    tfidf=corpus_vectors[index],
                    desc_tfidf=desc_vectors[index],
                    trigger_tfidf=trigger_vectors[index],
                )
            )

        edges = cls._build_edges(nodes)
        return cls(nodes, edges)

    @staticmethod
    def _discover_skills(source: Path) -> list[dict[str, Any]]:
        skill_files = []
        for path in source.rglob("SKILL.md"):
            skill_files.append(path)
        for path in source.rglob("skill.md"):
            skill_files.append(path)

        results: list[dict[str, Any]] = []
        seen: set[str] = set()
        unique_files: list[Path] = []
        for skill_file in skill_files:
            key = str(skill_file.resolve()).lower()
            if key in seen:
                continue
            seen.add(key)
            unique_files.append(skill_file)

        for skill_file in sorted(unique_files):
            raw = skill_file.read_text(encoding="utf-8")
            frontmatter, body = split_frontmatter(raw)
            name = str(frontmatter.get("name") or skill_file.parent.name)
            description = str(frontmatter.get("description") or "").strip()
            if not description:
                continue

            triggers = extract_trigger_lines(body)
            headings = extract_headings(body)
            requires_env, requires_bins, os_restrictions = extract_openclaw_metadata(frontmatter)
            code_refs = extract_code_refs(body)
            full_text = flatten_text(frontmatter, body)
            results.append(
                {
                    "id": normalize_id(name, skill_file.parent.name),
                    "name": name,
                    "description": description,
                    "version": frontmatter.get("version"),
                    "source_dir": str(skill_file.parent),
                    "source_file": str(skill_file),
                    "headings": headings,
                    "triggers": triggers,
                    "body_excerpt": body_excerpt(body),
                    "tool_mentions": code_refs,
                    "requires_env": requires_env,
                    "requires_bins": requires_bins,
                    "os_restrictions": os_restrictions,
                    "full_text_tokens": tokenize(full_text),
                    "description_tokens": tokenize(" ".join([name, description])),
                    "trigger_tokens": tokenize(" ".join(triggers) or description),
                    "keyword_tokens": tokenize(" ".join([name, description, *headings, *triggers])),
                }
            )
        return results

    @staticmethod
    def _build_edges(nodes: list[SkillNode]) -> list[SkillEdge]:
        pair_candidates: list[dict[str, Any]] = []
        for left_index in range(len(nodes)):
            for right_index in range(left_index + 1, len(nodes)):
                left = nodes[left_index]
                right = nodes[right_index]

                semantic_sim = 0.6 * cosine_similarity(left.desc_tfidf, right.desc_tfidf) + 0.4 * cosine_similarity(left.tfidf, right.tfidf)
                keyword_overlap = jaccard_similarity(set(left.keywords), set(right.keywords))
                tool_affinity = jaccard_similarity(
                    set(left.tool_mentions) | set(left.requires_bins),
                    set(right.tool_mentions) | set(right.requires_bins),
                )
                constraint_affinity = (
                    jaccard_similarity(set(left.requires_env), set(right.requires_env))
                    + jaccard_similarity(set(left.os_restrictions), set(right.os_restrictions))
                    + jaccard_similarity(set(left.requires_bins), set(right.requires_bins))
                ) / 3.0

                similar_score = 0.7 * semantic_sim + 0.3 * keyword_overlap
                substitute_score = 0.5 * semantic_sim + 0.2 * keyword_overlap + 0.2 * tool_affinity + 0.1 * constraint_affinity
                complementarity_proxy = clamp(
                    0.35 * tool_affinity
                    + 0.25 * constraint_affinity
                    + 0.15 * semantic_sim
                    + 0.15 * (1.0 - similar_score)
                    + 0.10 * (0.25 if tool_affinity >= similar_score else 0.05)
                )
                relation_scores = {
                    "similar": round(similar_score, 4),
                    "tool_affinity": round(tool_affinity, 4),
                    "constraint_affinity": round(constraint_affinity, 4),
                    "substitute": round(substitute_score, 4),
                }
                view_weights = {
                    "relation": round(max(relation_scores.values()), 4),
                    "similarity": round(similar_score, 4),
                    "complementarity": round(complementarity_proxy, 4),
                }

                active = {
                    key: value
                    for key, value in relation_scores.items()
                    if value >= {"similar": 0.12, "tool_affinity": 0.08, "constraint_affinity": 0.2, "substitute": 0.16}[key]
                }
                if not active:
                    continue

                dominant_relation = max(active, key=active.get)
                max_score = active[dominant_relation]
                evidence = [
                    f"semantic={semantic_sim:.3f}",
                    f"keyword={keyword_overlap:.3f}",
                    f"tool={tool_affinity:.3f}",
                    f"constraint={constraint_affinity:.3f}",
                    f"complementarity_proxy={complementarity_proxy:.3f}",
                ]
                pair_candidates.append(
                    {
                        "source": left.id,
                        "target": right.id,
                        "weight": round(max_score, 4),
                        "dominant_relation": dominant_relation,
                        "relation_scores": relation_scores,
                        "view_weights": view_weights,
                        "evidence": evidence,
                    }
                )

        neighbors_by_node: dict[str, list[dict[str, Any]]] = {node.id: [] for node in nodes}
        for candidate in pair_candidates:
            neighbors_by_node[candidate["source"]].append(candidate)
            neighbors_by_node[candidate["target"]].append(candidate)

        selected_pairs: set[tuple[str, str]] = set()
        for candidates in neighbors_by_node.values():
            ranked = sorted(candidates, key=lambda item: item["weight"], reverse=True)
            for candidate in ranked[:3]:
                pair_id = tuple(sorted((candidate["source"], candidate["target"])))
                selected_pairs.add(pair_id)

        edges: list[SkillEdge] = []
        for candidate in pair_candidates:
            pair_id = tuple(sorted((candidate["source"], candidate["target"])))
            if pair_id not in selected_pairs:
                continue
            edges.append(SkillEdge(**candidate))
        return edges

    def save(self, output_dir: Path) -> Path:
        output_dir.mkdir(parents=True, exist_ok=True)
        graph_path = output_dir / "graph.json"
        payload = {
            "nodes": [asdict(node) for node in self.nodes],
            "edges": [asdict(edge) for edge in self.edges],
            "stats": {
                "node_count": len(self.nodes),
                "edge_count": len(self.edges),
                "relation_counts": Counter(edge.dominant_relation for edge in self.edges),
            },
        }
        payload["stats"]["relation_counts"] = dict(payload["stats"]["relation_counts"])
        graph_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        self.graph_path = graph_path
        return graph_path

    @classmethod
    def load(cls, graph_path: Path) -> "GraphSkillEngine":
        payload = json.loads(graph_path.read_text(encoding="utf-8"))
        nodes = [SkillNode(**item) for item in payload["nodes"]]
        edges = [SkillEdge(**item) for item in payload["edges"]]
        return cls(nodes, edges, graph_path=graph_path)

    def query(self, task: str, *, top_k: int = 10) -> dict[str, Any]:
        query_tokens = tokenize(task)
        if not query_tokens:
            raise ValueError("Query task is empty after tokenization.")

        query_desc = normalized_tf(query_tokens)
        query_trigger = query_desc
        query_objects = {token for token in query_tokens if token not in ACTION_HINTS}
        query_keywords = set(top_keywords(list(query_objects) or query_tokens, limit=8))
        query_actions = {token for token in query_tokens if token in ACTION_HINTS}

        candidates = []
        for node in self.nodes:
            readiness_score, readiness_evidence = build_readiness(node)
            if readiness_score == 0.0:
                continue

            semantic_intent = cosine_similarity(query_desc, node.desc_tfidf)
            trigger_match = cosine_similarity(query_trigger, node.trigger_tfidf)
            object_match = jaccard_similarity(query_keywords, set(node.keywords))
            matched_keywords = query_keywords & set(node.keywords)
            specificity_score = len(matched_keywords) / max(len(set(node.keywords)), 1)
            lexical_match = len(query_keywords & set(tokenize(" ".join([node.name, node.description, *node.triggers])))) / max(len(query_keywords), 1)

            action_overlap = 0.0
            if query_actions:
                action_overlap = len(query_actions & set(node.tokens)) / len(query_actions)
            intent_match = 0.75 * semantic_intent + 0.25 * action_overlap

            if query_objects:
                body_object_overlap = jaccard_similarity(query_objects, set(node.tokens))
                object_match = 0.8 * object_match + 0.2 * body_object_overlap

            primary_score = (
                0.35 * intent_match
                + 0.20 * trigger_match
                + 0.15 * object_match
                + 0.10 * readiness_score
                + 0.10 * specificity_score
                + 0.10 * lexical_match
            )
            candidates.append(
                {
                    "node": node,
                    "score": round(primary_score, 4),
                    "intent_match": round(intent_match, 4),
                    "trigger_match": round(trigger_match, 4),
                    "object_match": round(object_match, 4),
                    "readiness_score": round(readiness_score, 4),
                    "specificity_score": round(specificity_score, 4),
                    "lexical_match": round(lexical_match, 4),
                    "readiness_evidence": readiness_evidence,
                }
            )

        candidates.sort(key=lambda item: item["score"], reverse=True)
        top_candidates = candidates[:top_k]
        if not top_candidates:
            return {"status": "no_match", "reason": "No runnable skills matched the query."}

        first = top_candidates[0]
        second_score = top_candidates[1]["score"] if len(top_candidates) > 1 else 0.0
        if first["score"] < 0.32:
            return {
                "status": "no_primary_skill",
                "reason": "Top candidate confidence is below threshold.",
                "candidates": [self._serialize_candidate(item) for item in top_candidates[:5]],
            }
        if first["score"] - second_score < 0.06:
            return {
                "status": "ambiguous",
                "reason": "Top candidates are too close to select a single primary skill.",
                "candidates": [self._serialize_candidate(item) for item in top_candidates[:5]],
            }

        primary = first["node"]
        supporting, fallbacks, similar = self._expand_neighbors(
            primary,
            query_desc=query_desc,
            query_trigger=query_trigger,
            query_keywords=query_keywords,
            query_objects=query_objects,
        )
        return {
            "status": "ok",
            "query": task,
            "primary_skill": self._serialize_candidate(first),
            "supporting_skills": supporting,
            "fallback_skills": fallbacks,
            "similar_skills": similar,
            "related_skills": supporting,
            "top_candidates": [self._serialize_candidate(item) for item in top_candidates[:5]],
        }

    def _expand_neighbors(
        self,
        primary: SkillNode,
        *,
        query_desc: dict[str, float],
        query_trigger: dict[str, float],
        query_keywords: set[str],
        query_objects: set[str],
    ) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
        edge_thresholds = {
            "similar": 0.14,
            "tool_affinity": 0.10,
            "constraint_affinity": 0.08,
            "substitute": 0.16,
        }
        relation_bonus = {
            "similar": 0.10,
            "tool_affinity": 0.70,
            "constraint_affinity": 0.55,
            "substitute": 0.20,
        }
        supporting: list[dict[str, Any]] = []
        fallbacks: list[dict[str, Any]] = []
        similar: list[dict[str, Any]] = []

        primary_keywords = set(primary.keywords) | set(primary.tokens)
        primary_tools = set(primary.tool_mentions) | set(primary.requires_bins)
        primary_constraints = set(primary.requires_env) | set(primary.requires_bins) | set(primary.os_restrictions)
        uncovered_query_terms = {token for token in query_keywords if token not in primary_keywords}

        for edge in self.adjacency.get(primary.id, []):
            neighbor_id = edge.target if edge.source == primary.id else edge.source
            neighbor = self.nodes_by_id[neighbor_id]
            readiness_score, readiness_evidence = build_readiness(neighbor)
            if readiness_score == 0.0:
                continue

            edge_type = edge.dominant_relation
            if edge.weight < edge_thresholds.get(edge_type, 0.1):
                continue

            neighbor_keywords = set(neighbor.keywords) | set(neighbor.tokens)
            neighbor_tools = set(neighbor.tool_mentions) | set(neighbor.requires_bins)
            neighbor_constraints = set(neighbor.requires_env) | set(neighbor.requires_bins) | set(neighbor.os_restrictions)

            query_desc_sim = cosine_similarity(query_desc, neighbor.desc_tfidf)
            query_trigger_sim = cosine_similarity(query_trigger, neighbor.trigger_tfidf)
            query_keyword_coverage = overlap_fraction(query_keywords, neighbor_keywords)
            task_relevance = clamp(
                0.45 * query_desc_sim
                + 0.25 * query_trigger_sim
                + 0.20 * query_keyword_coverage
                + 0.10 * readiness_score
            )

            uncovered_query_gain = overlap_fraction(uncovered_query_terms, neighbor_keywords)
            unique_neighbor_tools = neighbor_tools - primary_tools
            query_tool_hints = query_keywords | query_objects
            unique_tool_gain = overlap_fraction(query_tool_hints, unique_neighbor_tools)
            complementarity = clamp(
                0.40 * uncovered_query_gain
                + 0.30 * unique_tool_gain
                + 0.30 * relation_bonus.get(edge_type, 0.0)
            )

            tool_keyword_match = overlap_fraction(query_tool_hints, neighbor_tools)
            constraint_support = max(
                edge.relation_scores.get("constraint_affinity", 0.0),
                jaccard_similarity(primary_constraints, neighbor_constraints),
            )
            workflow_support = self._procedurality(neighbor)
            execution_support = clamp(
                0.35 * readiness_score
                + 0.25 * max(unique_tool_gain, tool_keyword_match)
                + 0.20 * constraint_support
                + 0.20 * workflow_support
            )

            desc_similarity = cosine_similarity(primary.desc_tfidf, neighbor.desc_tfidf)
            trigger_similarity = cosine_similarity(primary.trigger_tfidf, neighbor.trigger_tfidf)
            keyword_overlap = jaccard_similarity(set(primary.keywords), set(neighbor.keywords))
            tool_overlap = jaccard_similarity(primary_tools, neighbor_tools)
            redundancy_with_primary = clamp(
                0.50 * desc_similarity
                + 0.20 * trigger_similarity
                + 0.15 * keyword_overlap
                + 0.15 * tool_overlap
            )

            support_score = clamp(
                0.30 * task_relevance
                + 0.30 * complementarity
                + 0.25 * execution_support
                - 0.25 * redundancy_with_primary
            )

            shared_keywords = sorted((set(primary.keywords) & set(neighbor.keywords)) | (query_keywords & set(neighbor.keywords)))[:6]
            shared_tools = sorted(primary_tools & neighbor_tools)[:6]
            uncovered_hits = sorted(uncovered_query_terms & neighbor_keywords)[:6]
            relevant_unique_tools = sorted(unique_neighbor_tools & query_tool_hints)[:6]
            selection_reason = self._selection_reason(
                edge_type=edge_type,
                primary=primary,
                neighbor=neighbor,
                uncovered_query_terms=uncovered_query_terms,
                unique_neighbor_tools=set(relevant_unique_tools),
                shared_keywords=shared_keywords,
                shared_tools=shared_tools,
                task_relevance=task_relevance,
                complementarity=complementarity,
                execution_support=execution_support,
                redundancy_with_primary=redundancy_with_primary,
            )
            payload = {
                "id": neighbor.id,
                "name": neighbor.name,
                "description": neighbor.description,
                "edge_type": edge_type,
                "edge_weight": edge.weight,
                "support_score": round(support_score, 4),
                "task_relevance": round(task_relevance, 4),
                "complementarity": round(complementarity, 4),
                "execution_support": round(execution_support, 4),
                "redundancy_with_primary": round(redundancy_with_primary, 4),
                "selection_reason": selection_reason,
                "shared_keywords": shared_keywords,
                "shared_tools": shared_tools,
                "uncovered_query_terms_hit": uncovered_hits,
                "unique_neighbor_tools": relevant_unique_tools,
                "readiness_evidence": readiness_evidence,
            }
            if edge_type == "substitute":
                if task_relevance >= 0.28:
                    fallbacks.append(payload)
                continue

            if edge_type == "similar":
                if task_relevance >= 0.28:
                    similar.append(payload)
                continue

            if support_score < 0.08:
                continue
            if complementarity < 0.12:
                continue
            if redundancy_with_primary > 0.75:
                continue
            if not uncovered_hits and not relevant_unique_tools and edge_type == "tool_affinity":
                continue

            supporting.append(payload)

        supporting.sort(key=lambda item: item["support_score"], reverse=True)
        fallbacks.sort(key=lambda item: item["support_score"], reverse=True)
        similar.sort(key=lambda item: item["task_relevance"], reverse=True)
        return supporting[:3], fallbacks[:2], similar[:3]

    @staticmethod
    def _procedurality(node: SkillNode) -> float:
        procedural_headings = {
            "steps",
            "workflow",
            "quick start",
            "examples",
            "main commands",
            "basic workflow",
            "how to respond",
            "how to use",
        }
        heading_score = 1.0 if any(heading.lower() in procedural_headings for heading in node.headings) else 0.0
        trigger_score = min(len(node.triggers) / 4.0, 1.0)
        tool_score = min((len(node.tool_mentions) + len(node.requires_bins)) / 6.0, 1.0)
        excerpt_tokens = tokenize(node.body_excerpt)
        action_score = overlap_fraction(ACTION_HINTS, set(excerpt_tokens))
        return clamp(
            0.30 * tool_score
            + 0.25 * action_score
            + 0.25 * heading_score
            + 0.20 * trigger_score
        )

    @staticmethod
    def _selection_reason(
        *,
        edge_type: str,
        primary: SkillNode,
        neighbor: SkillNode,
        uncovered_query_terms: set[str],
        unique_neighbor_tools: set[str],
        shared_keywords: list[str],
        shared_tools: list[str],
        task_relevance: float,
        complementarity: float,
        execution_support: float,
        redundancy_with_primary: float,
    ) -> str:
        reasons: list[str] = []
        if uncovered_query_terms:
            hit_terms = sorted(uncovered_query_terms & (set(neighbor.keywords) | set(neighbor.tokens)))
            if hit_terms:
                reasons.append(
                    f"It covers query aspects the primary skill does not emphasize yet: {', '.join(hit_terms[:4])}."
                )
        if unique_neighbor_tools:
            reasons.append(
                f"It adds execution-specific tools or assets that the primary skill does not expose: {', '.join(sorted(unique_neighbor_tools)[:4])}."
            )
        if edge_type == "tool_affinity":
            reasons.append("Its strongest relation to the primary skill comes from overlapping implementation tools or code references.")
        elif edge_type == "constraint_affinity":
            reasons.append("It appears compatible with the same runtime constraints, so it can reinforce execution setup or formatting boundaries.")
        if shared_keywords and not reasons:
            reasons.append(f"It stays relevant to the same task area through shared concepts such as {', '.join(shared_keywords[:4])}.")
        if shared_tools and not reasons:
            reasons.append(f"It shares execution mechanisms with the primary skill via {', '.join(shared_tools[:4])}.")
        if not reasons:
            reasons.append(
                f"It remains relevant to `{primary.name}` while contributing a slightly different angle for `{neighbor.name}`."
            )
        reasons.append(
            f"Scoring summary: task relevance={task_relevance:.2f}, complementarity={complementarity:.2f}, execution support={execution_support:.2f}, redundancy penalty={redundancy_with_primary:.2f}."
        )
        return " ".join(reasons)

    @staticmethod
    def _serialize_candidate(candidate: dict[str, Any]) -> dict[str, Any]:
        node: SkillNode = candidate["node"]
        return {
            "id": node.id,
            "name": node.name,
            "description": node.description,
            "score": candidate["score"],
            "intent_match": candidate["intent_match"],
            "trigger_match": candidate["trigger_match"],
            "object_match": candidate["object_match"],
            "readiness_score": candidate["readiness_score"],
            "specificity_score": candidate["specificity_score"],
            "lexical_match": candidate["lexical_match"],
            "source_dir": node.source_dir,
            "readiness_evidence": candidate["readiness_evidence"],
        }
