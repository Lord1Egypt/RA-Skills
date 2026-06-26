---
name: research-papers
description: Search academic papers and conduct literature reviews using the OpenAlex API, personalized for dynamic functional brain networks, rs-fMRI/fMRI neuroimaging, graph neural networks, spatiotemporal attention, Alzheimer's disease, mild cognitive impairment, Parkinson's disease, and neurodegenerative disease classification. Use when the user needs paper search, DOI lookup, citation analysis, open-access PDF discovery/download, or literature review generation. If the request is vague, assume the default research context is dynamic brain network modeling for neurodegenerative disease classification.
---

# Academic Research

Search academic works via OpenAlex. No API key required.

This skill is personalized for the user's research direction: dynamic brain network modeling, rs-fMRI/fMRI, graph neural networks, spatiotemporal attention, and neurodegenerative disease classification.

Originally based on an academic-research workflow and adapted for neuroimaging literature search.

## Default Research Profile

When the user asks for papers, related work, recent methods, baselines, or literature reviews without giving a full topic, assume the default research context is:

- Dynamic functional brain networks
- rs-fMRI / fMRI neuroimaging
- Dynamic functional connectivity
- Alzheimer's disease, MCI, and Parkinson's disease
- Neurodegenerative disease classification
- Graph neural networks for brain networks
- Spatiotemporal attention and temporal-spatial interaction
- Cross-time-slice dynamic brain state modeling

Do not ask the user to repeat this research direction unless the request is ambiguous across fields.

## Query Expansion Rules

When the user gives a short or Chinese query, expand it into English academic search terms before calling OpenAlex.

Examples:

- "recent papers" → `dynamic functional brain network rs-fMRI graph neural network neurodegenerative disease classification`
- "AD classification" → `Alzheimer's disease classification mild cognitive impairment rs-fMRI dynamic functional connectivity graph neural network`
- "brain network GNN" → `functional brain network dynamic brain connectivity GCN GAT graph neural network disease diagnosis`
- "时空注意力" → `spatiotemporal attention dynamic brain network fMRI temporal-spatial interaction neurodegenerative disease classification`
- "动态脑网络论文" → `dynamic functional brain network dynamic functional connectivity rs-fMRI graph neural network Alzheimer's disease classification`

If the user gives a specific DOI, author, paper title, or clearly defined topic, do not over-expand.

## Language Behavior

The user may ask in Chinese.

For Chinese requests:

1. Translate or expand the search query into English academic keywords.
2. Return explanations in Chinese unless the user asks for English.
3. Explain why each selected paper is relevant to the user's research direction.

## Quick Start

### Search papers by topic

```bash
python scripts/scholar-search.py search "dynamic functional brain network Alzheimer's disease graph neural network" --limit 10 --years 2020-2026
```

### Search rs-fMRI and disease classification papers

```bash
python scripts/scholar-search.py search "rs-fMRI graph neural network neurodegenerative disease classification" --limit 10 --years 2020-2026
```

### Search spatiotemporal attention papers

```bash
python scripts/scholar-search.py search "spatiotemporal attention dynamic brain network fMRI" --limit 10 --years 2020-2026
```

### Search by author

```bash
python scripts/scholar-search.py author "Yann LeCun" --limit 5
```

### Look up by DOI

```bash
python scripts/scholar-search.py doi "10.1038/s41586-021-03819-2"
```

### Get citation chain

```bash
python scripts/scholar-search.py citations "10.1038/s41586-021-03819-2" --direction both
```

### Deep read

```bash
python scripts/scholar-search.py deep "10.1038/s41586-021-03819-2"
```

## New Features

### Cache

API responses are cached locally to reduce repeated requests.

Useful options:

- `--no-cache`
- `--refresh-cache`
- `--cache-ttl N`

Example:

```bash
python scripts/scholar-search.py --refresh-cache search "dynamic functional brain network Alzheimer's disease" --limit 10
```

### Open-Access PDF Download

Use `--download-pdf` to download PDFs only when they are legally available from open-access sources.

```bash
python scripts/scholar-search.py search "dynamic functional brain network Alzheimer's disease" --limit 5 --oa --download-pdf
```

Do not bypass paywalls or use unauthorized sources.

### QQBot Handoff

For long literature reviews, generate a Markdown review file and send it through `qqbot-send`:

```bash
python scripts/scholar-search.py review "dynamic functional brain networks in Alzheimer's disease" --papers 30 --years 2020-2026 --qqmedia
```

If needed, specify the staging script manually:

```bash
python scripts/scholar-search.py review "dynamic brain network Alzheimer's disease" --papers 20 --qqmedia --stage-media-script "../qqbot-send/scripts/stage_media.py"
```

## Literature Review Workflow

Generate a Markdown literature review:

```bash
python scripts/scholar-search.py review "dynamic functional brain networks in Alzheimer's disease" --papers 30 --years 2020-2026 --output review.md
```

This will:

1. Search across multiple query variations.
2. Deduplicate and rank papers.
3. Identify thematic clusters.
4. Generate a structured Markdown synthesis.
5. Optionally download open-access PDFs.
6. Optionally hand off the review file to QQBot.

Options:

- `--papers N` — Target number of papers.
- `--output FILE` — Write review to file.
- `--years 2020-2026` — Restrict publication years.
- `--json` — Output JSON.
- `--oa` — Open-access papers only.
- `--download-pdf` — Download open-access PDFs.
- `--qqmedia` — Generate a file and output a `<qqmedia>...</qqmedia>` tag.

## Preferred Output

When presenting paper results, include:

- Title
- Year
- Authors
- Source
- Citation count
- DOI
- Open-access URL or PDF URL if available
- Why the paper is relevant to the user's research

For literature reviews, organize by:

- Research background
- Main methods
- Representative papers
- Model architectures
- Dynamic brain network modeling strategies
- Limitations
- Relevance to the user's own research

When the result is long, prefer generating a Markdown file and using `--qqmedia`.

## Output Format

Search commands return structured data including:

- Title and year
- Authors
- Abstract
- Citation count
- DOI
- Open-access URL
- PDF URL or downloaded PDF path
- Source journal/venue
- OpenAlex ID

## Tips

- Use `--sort citations` for highly cited papers.
- Use `--sort recent` for newer papers.
- Use `--oa --download-pdf` when the user wants downloadable full text.
- Use `review --qqmedia` when the literature review is too long for direct chat output.