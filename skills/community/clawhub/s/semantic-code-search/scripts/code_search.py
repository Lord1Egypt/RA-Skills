"""
Semantic Code Search Engine — intent-based code retrieval
AgentBounty: CodeIndex Labs $4,500
"""
import ast
import json
import hashlib
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
from collections import defaultdict


@dataclass
class CodeFragment:
    file_path: str
    start_line: int
    end_line: int
    name: str
    code: str
    docstring: str = ""
    frag_type: str = "function"  # function, class, method
    embedding: list[float] = field(default_factory=list)
    id: str = ""

    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(f"{self.file_path}:{self.start_line}:{self.name}".encode()).hexdigest()[:12]

    @property
    def search_text(self) -> str:
        """Combined text for embedding/search."""
        parts = [f"{self.frag_type} {self.name}"]
        if self.docstring:
            parts.append(self.docstring)
        # Add variable names and call names from the code
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                    parts.append(f"calls:{node.func.id}")
                if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                    parts.append(f"sets:{node.id}")
        except SyntaxError:
            pass
        return " ".join(parts)


class ASTParser:
    """Extract code fragments from Python files using AST."""

    def parse_file(self, path: Path) -> list[CodeFragment]:
        try:
            source = path.read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError):
            return []

        fragments = []
        source_lines = source.splitlines()

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                docstring = ast.get_docstring(node) or ""
                start = node.lineno
                end = node.end_lineno or start
                code = "\n".join(source_lines[start - 1:end])
                fragments.append(CodeFragment(
                    file_path=str(path), start_line=start, end_line=end,
                    name=node.name, code=code, docstring=docstring,
                    frag_type="method" if isinstance(getattr(node, 'parent', None), ast.ClassDef) else "function"
                ))
            elif isinstance(node, ast.ClassDef):
                docstring = ast.get_docstring(node) or ""
                start = node.lineno
                end = node.end_lineno or start
                code = "\n".join(source_lines[start - 1:end])
                fragments.append(CodeFragment(
                    file_path=str(path), start_line=start, end_line=end,
                    name=node.name, code=code, docstring=docstring, frag_type="class"
                ))

        return fragments

    def parse_directory(self, root: Path, extensions: set[str] = None) -> list[CodeFragment]:
        extensions = extensions or {".py"}
        fragments = []
        for path in root.rglob("*"):
            if path.suffix in extensions and not any(p.startswith(".") for p in path.relative_to(root).parts):
                fragments.extend(self.parse_file(path))
        return fragments


class SimpleVectorizer:
    """Bag-of-words vectorizer with TF-IDF-like scoring (no ML dependency)."""

    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.dim = 0

    def fit(self, texts: list[str]):
        # Build vocabulary
        word_set = set()
        doc_freq = defaultdict(int)
        for text in texts:
            words = set(text.lower().split())
            word_set.update(words)
            for w in words:
                doc_freq[w] += 1
        self.vocab = {w: i for i, w in enumerate(sorted(word_set))}
        self.dim = len(self.vocab)
        n = len(texts)
        self.idf = {w: n / (df + 1) for w, df in doc_freq.items()}

    def transform(self, text: str) -> list[float]:
        if not self.vocab:
            return []
        vec = [0.0] * self.dim
        words = text.lower().split()
        for w in words:
            if w in self.vocab:
                vec[self.vocab[w]] += 1.0 * self.idf.get(w, 1.0)
        # Normalize
        norm = sum(v * v for v in vec) ** 0.5
        if norm > 0:
            vec = [v / norm for v in vec]
        return vec


class CodeIndex:
    """Index a codebase for semantic search."""

    def __init__(self, root_path: str, extensions: set[str] = None):
        self.root = Path(root_path)
        self.parser = ASTParser()
        self.vectorizer = SimpleVectorizer()
        self.fragments: list[CodeFragment] = []
        self.extensions = extensions or {".py", ".js", ".ts"}

    def build(self):
        self.fragments = self.parser.parse_directory(self.root, self.extensions)
        texts = [f.search_text for f in self.fragments]
        self.vectorizer.fit(texts)
        for frag in self.fragments:
            frag.embedding = self.vectorizer.transform(frag.search_text)
        return len(self.fragments)

    def save(self, path: str):
        data = [{
            "id": f.id, "file": f.file_path, "start": f.start_line, "end": f.end_line,
            "name": f.name, "type": f.frag_type, "docstring": f.docstring, "code": f.code,
        } for f in self.fragments]
        Path(path).write_text(json.dumps(data, indent=2))


class SemanticSearch:
    """Search the code index by intent or similarity."""

    def __init__(self, index: CodeIndex):
        self.index = index

    def _cosine(self, a: list[float], b: list[float]) -> float:
        if not a or not b or len(a) != len(b):
            return 0.0
        dot = sum(x * y for x, y in zip(a, b))
        na = sum(x * x for x in a) ** 0.5
        nb = sum(x * x for x in b) ** 0.5
        return dot / (na * nb) if na and nb else 0.0

    def query(self, text: str, limit: int = 10, min_score: float = 0.1) -> list[dict]:
        q_vec = self.index.vectorizer.transform(text)
        scored = []
        for frag in self.index.fragments:
            score = self._cosine(q_vec, frag.embedding)
            if score >= min_score:
                scored.append((score, frag))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": f.id, "name": f.name, "file": f.file_path, "line": f.start_line,
                 "type": f.frag_type, "docstring": f.docstring[:100], "score": round(s, 3)}
                for s, f in scored[:limit]]

    def similar_to(self, fragment_id: str, limit: int = 10) -> list[dict]:
        target = next((f for f in self.index.fragments if f.id == fragment_id), None)
        if not target:
            return []
        scored = []
        for frag in self.index.fragments:
            if frag.id == fragment_id:
                continue
            score = self._cosine(target.embedding, frag.embedding)
            if score > 0.1:
                scored.append((score, frag))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [{"id": f.id, "name": f.name, "file": f.file_path, "score": round(s, 3)}
                for s, f in scored[:limit]]

    def duplicates(self, threshold: float = 0.85) -> list[dict]:
        """Find near-duplicate code fragments."""
        dups = []
        for i, a in enumerate(self.index.fragments):
            for b in self.index.fragments[i + 1:]:
                score = self._cosine(a.embedding, b.embedding)
                if score >= threshold:
                    dups.append({"a": a.id, "a_name": a.name, "b": b.id, "b_name": b.name, "score": round(score, 3)})
        return dups


if __name__ == "__main__":
    import click

    @click.group()
    def cli():
        pass

    @cli.command()
    @click.argument("path")
    def index(path):
        idx = CodeIndex(path)
        n = idx.build()
        click.echo(f"Indexed {n} fragments from {path}")
        idx.save(".code_index.json")

    @cli.command()
    @click.argument("query")
    def query(query):
        idx = CodeIndex(".")
        idx.build()
        search = SemanticSearch(idx)
        results = search.query(query)
        for r in results:
            click.echo(f"  {r['score']:.3f} {r['type']} {r['name']} ({r['file']}:{r['line']})")

    cli()
