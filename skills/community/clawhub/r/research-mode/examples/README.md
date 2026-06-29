# Research Mode Examples

These examples are generated outputs from bounded Research Mode tasks. They are
intended for repository review, regression checks, and demonstration of expected
deliverable shapes.

## How To Read These Examples

Each directory is a public-safe snapshot of a completed or review-ready Research
Mode task. Start with the human-facing output files, then inspect
`research-trace/` if you want to understand how the task moved through
iterations, evidence collection, verification, and finalization.

The trace is intentionally not a raw task directory. It is a sanitized copy of
state, runs, result payloads, iteration notes, source/finding logs, playbooks,
and selected analysis artifacts that are useful for review without exposing
private workspace paths or chat identifiers.

## Showcase

### `web-capture-evaluation/`

This example demonstrates a safe web-to-Markdown capture workflow for agent
research. It is useful if you want to inspect how Research Mode frames external
web content as untrusted evidence, separates capture from analysis, and turns a
workflow into a reviewable Markdown package.

Start here:

- `README.md` for the package overview.
- `final-report.md` for the synthesized result.
- `research-plan.md` for the step-by-step workflow.
- `research-trace/` for task state, iterations, result payloads, and selected
  verification artifacts.

### `rag-eval-tooling-matrix/`

This example demonstrates a source-backed decision package for choosing RAG and
LLM application evaluation tooling. It includes Markdown notes, a validation
report, public evidence links, and a non-trivial XLSX workbook.

ClawHub installs only text-like files from skill packages. If you installed
Research Mode through `clawhub install`, the Markdown reports, sources,
validation notes, and sanitized trace are present, but the XLSX workbook is not.
Use the GitHub repository or GitHub release package when you need
`rag-eval-tooling-matrix.xlsx`.

Start here:

- `README.md` for the package overview.
- `final-report.md` for the recommendation.
- `rag-eval-tooling-matrix.xlsx` for the scoring workbook in the GitHub
  checkout/release package.
- `validation-report.md` for workbook checks.
- `research-trace/` for task state, iterations, result payloads, source/finding
  logs, and selected analysis artifacts.

## Available Examples

- `web-capture-evaluation/` - five-file Markdown package for safe
  web-to-Markdown capture in agent research workflows.
- `rag-eval-tooling-matrix/` - public-source RAG evaluation tooling decision
  package with Markdown notes, validation report, and a non-trivial XLSX
  workbook.

Each example also contains `research-trace/`, a sanitized copy of the task
state, runs, iteration notes, result payloads, source/finding logs, playbook, and
selected task-local analysis artifacts. These traces show how the workflow moved
from research to verification and review-gated finalization.

The examples should not contain private workspace paths, chat identifiers,
tokens, personal context, or raw internal task state. If an example is generated
from a live task, copy only the reviewed output package, not the task directory.
