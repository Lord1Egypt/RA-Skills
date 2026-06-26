---
name: owl
description: >
  6-step structured research skill. Searches arXiv, reads 5 papers via markitdown,
  has Claude select the best 2, runs 4 targeted web searches (explanation, GitHub,
  survey, citations), then writes a 5-bullet summary. Use when a user asks for a
  "research summary", "deep dive", "what is X", "find papers on Y", "owl research",
  or any query that benefits from both academic papers and web context combined into
  a concise, citation-backed summary.
metadata:
  openclaw:
    requires:
      env:
        - OPENROUTER_API_KEY
        - SERPER_API_KEY
      bins:
        - python
---

# 🦉 OWL — 6-Step Research Skill

A precise, structured research pipeline — not a bulk dump, but a curated read-and-select
workflow that mirrors how an expert researcher actually works.

---

## Pipeline

```
Step 1 · Search arXiv for the topic
Step 2 · Open 5 promising papers → PDF → Markdown via markitdown
Step 3 · Read title + abstract + intro of each
Step 4 · Claude selects the best 2 (explains why, drops the rest)
Step 5 · Search web: explanation · GitHub · survey · citations
Step 6 · Write a 5-bullet summary of what was learned
```

---

## Install

```bash
pip install requests markitdown
pip install curl_cffi beautifulsoup4 lxml fake-useragent
chmod +x scripts/owl.py
cp scripts/owl.py /usr/local/bin/owl


```

---

## Usage

```bash
owl "diffusion models"
owl "LoRA fine-tuning" --category cs.LG --output report.md
owl "protein structure prediction" --since year
owl "quantum error correction" --arxiv-n 8
```
For Windows user: 
```
python  scripts/owl.py "AI agent RAG" --arxiv-n 8 --output report.md
```
---

## CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `query` | *(required)* | Research topic |
| `--arxiv-n N` | 5 | arXiv candidates to fetch (top N are used as pool) |
| `--category CAT` | all | arXiv category, e.g. `cs.LG`, `q-bio.BM` |
| `--sort` | relevance | `relevance`, `lastUpdatedDate`, `submittedDate` |
| `--since RANGE` | all time | Google recency: `hour`, `day`, `week`, `month`, `year` |
| `--papers-dir DIR` | `/tmp/owl_papers` | PDF + markdown cache directory |
| `--output FILE` | terminal only | Save Markdown summary to FILE |
| `--no-stream` | off | Wait for full Claude response |
| `--serper-key KEY` | env var | Override `SERPER_API_KEY` |
| `--anthropic-key KEY` | env var | Override `ANTHROPIC_API_KEY` |

---

## Step Details

### Step 1 — arXiv Search
`search_arxiv(query, n, category, sort_by)` → list of paper dicts with
`id, title, authors, abstract, published, categories, url, pdf_url`.

### Step 2 — Open Papers (PDF → Markdown)
Take top 5 candidates. For each: download PDF to `--papers-dir`, convert to
Markdown using `markitdown` (Python lib preferred, CLI fallback). Extract first
8 KB of text = roughly title + abstract + introduction. Falls back to abstract
only if PDF download or conversion fails.

### Step 3 — Read
Display truncated abstract+intro for each candidate. All 5 intro texts are
passed to Claude in Step 4.

### Step 4 — LLM Selects Best 2 papers
Claude returns `{"selected": [i, j], "reason_1": "...", "reason_2": "...",
"dropped": "..."}`. The model used is printed in the step output and checklist.
Selected papers then get their **full** markdown (up to 40 KB) loaded for Step 6.

### Step 5 — 4 Web Searches
Runs 4 targeted Serper queries and fetches page content for the top 2 results
of each:

| Search type | Query pattern |
|-------------|---------------|
| explanation | `{topic} explained` |
| github | `{topic} github implementation` |
| survey | `{topic} survey review paper` |
| citations | `{topic} highly cited papers results` |

### Step 6 — 5-Bullet Summary
Builds a prompt with both full papers + all 4 web search result sets, then
calls LLM api. Output structure:

1. Selected Papers (with links)
2. **5 dense bullets** — each 3–5 sentences, specific facts, inline citations
3. Web Sources list

---

## Output Format

```markdown
# 🦉 OWL Research Summary: {topic}

## Selected Papers
[P1] Title — Authors — URL — PDF
[P2] Title — Authors — URL — PDF

## 5-Bullet Summary
• **What it is**: ...
• **How it works**: ...
• **Key results**: ...
• **Tools & code**: ...
• **Open questions**: ...

## Web Sources
...
```

---

## Steps Checklist Verification

At the end of every run, owl prints a checklist confirming every step completed
successfully. Verify all 6 items are marked `[✓]` before trusting the output.

```
────────────────────────────────────────────────────────────────────────
  ✅ RESEARCH CHECKLIST
────────────────────────────────────────────────────────────────────────
  [✓] Step 1  Search arXiv                  5 papers found
  [✓] Step 2  Open 5 papers via markitdown   5 PDFs converted
  [✓] Step 3  Read title + abstract + intro  5 papers scanned
  [✓] Step 4  Keep best 2                    2 selected  (2 with full text)
              → Paper title one…
              → Paper title two…
  [✓] Step 5  Web search (4 queries)         16 results fetched
              → explanation    Top result title…
              → github         Top result title…
              → survey         Top result title…
              → citations      Top result title…
  [✓] Step 6  5-bullet summary               written by Claude
              → /path/to/report.md
────────────────────────────────────────────────────────────────────────
```

### What each line confirms

| Step | What to verify |
|------|---------------|
| Step 1 | At least 1 paper found — if 0, the arXiv query returned nothing; try rephrasing or removing `--category` |
| Step 2 | PDFs converted — a `⚠ using abstract only` warning here means markitdown failed for that paper; the run continues but that paper's selection is abstract-only |
| Step 3 | Count matches Step 2 — should always be 5 (or `--arxiv-n` if overridden) |
| Step 4 | Exactly 2 selected, model name visible — the model shown is whatever `GET /v1/models` returned as the best available; if it shows the fallback `claude-sonnet-4-20250514` the models list API may have failed silently |
| Step 5 | 4 search types listed, each with a top result — a missing type means that Serper query failed silently |
| Step 6 | "written by Claude" confirms the API call completed — if the summary is truncated, raise `max_tokens` in the source |

### Failure modes to watch for

- **Step 2 all `⚠`** — `markitdown` is not installed (`pip install markitdown`) or PDFs are blocked by arXiv rate limiting; wait and retry
- **Step 4 shows 1 paper** — Claude JSON parse failed; re-run or check `OPENROUTER_API_KEY`
- **Step 5 shows 0 results for a type** — Serper key exhausted or network issue; check `SERPER_API_KEY`
- **Step 6 summary is very short** — context window may be near limit with large PDFs; reduce `--arxiv-n` or use `--no-stream`

---

## Notes

- PDFs are cached in `--papers-dir` — re-runs on the same paper are instant
- Step 4 uses a non-streaming JSON call; Steps 2 and 6 stream to terminal
- `--arxiv-n` can be raised to 8–10 for broader candidate pools before selection
- All 4 web search types always run — they cannot be individually disabled (by design)
- The 5-bullet format is enforced in the Claude prompt; free-form reports use the old pipeline
