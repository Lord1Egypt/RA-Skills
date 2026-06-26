---
name: research-briefing
description: Build a focused literature and citation briefing from PapersFlow. Use when the user wants paper search, citation verification, related-paper discovery, or citation graph exploration.
---

# Research Briefing

Use this skill when a user wants a high-signal research briefing grounded in the hosted `papersflow-mcp` server.

## Workflow

1. Resolve the user's target topic, title, DOI, or seed paper.
2. Start with `search_literature` for broad discovery.
3. Use `verify_citation` when the user gives a citation string, DOI, URL, PubMed ID, arXiv ID, or uncertain bibliographic reference.
4. Use `find_related_papers` when the user wants nearby work around a seed paper.
5. Use `get_citation_graph` when the user wants a graph view with references, incoming citations, and optionally similar papers.
6. Use `get_paper_neighbors` when the user wants a one-hop grouped view instead of a graph-first view.
7. Use `expand_citation_graph` only after you already have seed node ids from a previous graph result.
8. Use `fetch` when the user wants a richer single-paper record after search or graph exploration.

## Output Style

- Prefer short grouped sections over long prose.
- Include paper titles, years, identifiers, and why they matter.
- If the user asked for a graph-oriented answer, explicitly distinguish:
  - references
  - later citations
  - similar papers
- If the graph result looks noisy, say so instead of pretending the neighborhood is authoritative.

## Tool Guidance

### Use `search_literature`

Use for:

- topic exploration
- early-stage paper discovery
- short lists of candidate seed papers

### Use `verify_citation`

Use for:

- checking a citation string
- normalizing a DOI or paper URL
- producing a reliable paper identifier before deeper exploration

### Use `get_citation_graph`

Use for:

- seed-centered graph exploration
- showing how a paper connects to prior and later work

Prefer this when the user explicitly asks for a graph, network, map, or influence chain.

### Use `get_paper_neighbors`

Use for:

- concise grouped neighbors
- "show me the references / citations / similar papers" requests

Prefer this over the graph tool when the user cares more about grouped lists than graph structure.

### Use `expand_citation_graph`

Use only when:

- you already have valid node ids from a previous graph result
- the user wants to grow the graph one hop farther

Do not guess node ids.

## Examples

- User asks: "Find five strong papers on retrieval-augmented generation evaluation and tell me which one to start with."
- User asks: "Verify this citation and give me a normalized version."
- User asks: "Show me the citation graph around Attention Is All You Need."
- User asks: "Expand the graph from these two node ids and tell me where the important branches are."
