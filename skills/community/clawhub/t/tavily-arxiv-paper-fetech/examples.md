# Tavily arXiv Paper Fetech Examples

## Single title

```text
/tavily-arxiv-paper-fetech "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control --workdir 0_docs/tavily_arxiv_lookup_rt2"
```

## Multiple titles

```text
/tavily-arxiv-paper-fetech "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control
OpenVLA: An Open-Source Vision-Language-Action Model
Language Models (Mostly) Know What They Know --workdir 0_docs/tavily_arxiv_lookup_batch_01"
```

## Expected work folder layout

```text
WORKDIR/
├── input_titles.md
├── paper_fetches.jsonl
└── paper_fetch_report.md
```

## JSONL line shape

Each processed title should append one JSON line like:

```json
{
  "index": 1,
  "input_title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
  "tavily_status": "ok",
  "tavily_error": null,
  "arxiv_url": "https://arxiv.org/abs/2307.15818",
  "fetch": {
    "canonical_abs_url": "https://arxiv.org/abs/2307.15818",
    "arxiv_id": "2307.15818",
    "title": "RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control",
    "authors": ["..."],
    "abstract": "..."
  }
}
```

## Tavily-only rule

- title resolution uses Tavily only
- if Tavily rate limits, retry Tavily only
- do not switch to arXiv search, arXiv API search, guessed URLs, or another provider
