# Research & Knowledge (OpenClaw Optimized)

This reference defines high-performance research and knowledge management workflows for AI agents in the OpenClaw environment, merging real-time web discovery with structured synthesis.

## 1. Deep Research Methodology

### The Ryder Research Loop
1. **Orientation**: Use `web_search` with 3-5 seed queries to map the landscape.
2. **Deep Dive**: Use `web_fetch` on authoritative URLs (primary sources).
3. **Parallel Research**: Use `subagent spawn` to research specific sub-topics in parallel.
4. **Synthesis**: Build a `RESEARCH_BRIEF.md` in the workspace.

---

## 2. Knowledge Graph & RAG

### Building a Local Knowledge Base
- **Entity Extraction**: Use `read` and `exec` (Python/Grep) to extract People, Organizations, and Concepts from a document corpus.
- **RAG Preparation**: 
  1. **Chunking**: Use `exec` with a Python script to chunk large `.txt` or `.md` files.
  2. **Storage**: Save high-value context to the `memory/` directory for long-term retrieval.
  3. **Evaluation**: Periodically run a `rag_eval.py` script to check the "Faithfulness" of generated answers.

---

## 3. Content Extraction & Synthesis

### Multi-Source Ingestion
- **Web Articles**: Use `web_fetch` to extract clean markdown/text.
- **PDFs**: Use `exec` with `pdftotext` to convert research papers.
- **YouTube**: Use `web_search` to find video transcripts or `exec` with `yt-dlp` if available.
- **Synthesis**: Group findings by "Consensus" vs. "Contested" areas.

---

## 4. Data Exploration & Profiling

### Automated Data Audit
- **Profiling**: Use `exec` with Python (`pandas.describe()`) to profile CSV/JSON datasets.
- **Quality Check**: Flag null rates, outliers, and schema inconsistencies.
- **Visualization**: Use `exec` with `matplotlib` or `seaborn` to generate charts and save them to the `assets/` directory.

---

## 5. Statistical Analysis

### Business Intelligence Workflows
- **Metrics**: Calculate Growth Rates (YoY, CAGR) and Moving Averages.
- **Outliers**: Use the IQR (Interquartile Range) method via Python to detect and flag anomalies.
- **Hypothesis Testing**: Run t-tests or Chi-squared tests to validate A/B test results.

---

## 6. Creative Ideation & Brainstorming

### The "Design First" Gate
- **Hard Gate**: Never implement a research plan before the user approves a `DESIGN.md`.
- **Techniques**: Use Lateral Thinking and Pre-mortem analysis to identify blind spots in the research scope.

---
*Derived from Perplexity Super-Skills & Claude Code. Optimized for OpenClaw by Ryder.*
