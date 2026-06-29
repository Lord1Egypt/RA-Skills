# RAG Evaluation Tooling Matrix

This example package compares current RAG and LLM application evaluation tooling for a production RAG project. It is designed as a compact public-safe decision aid: every tool row is backed by public evidence links, and the workbook separates evaluation capability from deployment and governance fit.

## Included files

- `rag-eval-tooling-matrix.xlsx` - Excel workbook with Summary, Tool Matrix, Scoring, Evidence Sources, Exclusions Caveats, and Methodology sheets. This binary workbook is included in the GitHub checkout/release package, but not in text-only ClawHub installs.
- `final-report.md` - human-readable analysis and recommendation notes.
- `sources.md` - public evidence index used by the workbook.
- `validation-report.md` - workbook structure and compatibility checks from generation time.

## How to use the workbook

1. Start in the Summary sheet for the shortlist.
2. Use Tool Matrix to compare evaluation fit, operational fit, and caveats.
3. Adjust 0-5 criterion scores if your project has different constraints.
4. Review Evidence Sources and Exclusions Caveats before treating a score as procurement-ready.

The matrix is intentionally not a benchmark. It scores documented fit, public evidence maturity, and production adoption risk.

## Short take

- For managed or enterprise-heavy teams, start with LangSmith, Langfuse, Phoenix, W&B Weave, Opik, or MLflow GenAI depending on your existing stack.
- For CI/regression-first workflows, compare DeepEval / Confident AI and Promptfoo.
- For RAG metric depth, consider Ragas and TruLens, usually paired with a separate tracking or observability layer.
- For framework-native projects, LlamaIndex and Haystack evaluators are useful when the app already uses those frameworks.
- Treat OpenAI Evals / Evals API as legacy because official OpenAI docs now describe a deprecation and shutdown timeline.

Generated on 2026-06-16 from public sources.
