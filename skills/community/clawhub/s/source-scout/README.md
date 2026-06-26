# Source Scout

Source Scout is an OpenClaw skill for answering factual “random knowledge” questions with a better default workflow:

1. search the web,
2. cross-check the core facts,
3. cite reliable sources,
4. include a sourced image/photo/figure when useful.

It exists because quick factual answers are often where assistants silently hallucinate or omit provenance. Source Scout makes grounding the default without turning every answer into a long research report.

## When to use it

Use Source Scout for questions like:

- “Where are the cells that die in Parkinson’s located?”
- “Why is the sky blue?”
- “Who discovered CRISPR?”
- “How does lithium-ion battery degradation work?”
- “What changed in the latest WHO guideline?”

It is especially useful for:

- science and medicine explainers,
- history/geography facts,
- current or mutable facts,
- anything where a diagram, map, photograph, or paper figure improves understanding.

## What it does

The skill tells the agent to:

- run web search before answering from memory;
- prefer authoritative sources such as official institutions, NCBI/PubMed/PMC, review papers, government/health agencies, and reputable educational resources;
- cite 2–5 high-quality sources;
- look for an existing online figure/photo/diagram before generating a custom image;
- prefer open-license or official educational imagery;
- download images locally before attaching them when the runtime supports media attachments, because raw external media URLs may not render reliably in some clients.

## Example answer shape

```text
Short answer: ...

- Key point 1...
- Key point 2...

[image attachment or image link]

Sources:
- Source name — https://example.org/...
- Source name — https://example.org/...
```

## Installation

Install from ClawHub once published:

```bash
clawhub install source-scout
```

Or copy this folder into your OpenClaw skills directory:

```bash
cp -R source-scout ~/.openclaw/workspace/skills/source-scout
openclaw skills check
```

## Files

```text
source-scout/
├── SKILL.md
├── README.md
└── agents/
    └── openai.yaml
```

## License

MIT-0 / MIT No Attribution. ClawHub skills are published under MIT-0 terms.
