# Web Capture Example: Synthesis Scaffold

This scaffold narrows the prior workflow map into the five-file public package
requested for `examples/web-capture-evaluation/`. It is an intermediate
analysis artifact, not the final package.

## Package intent

The example should let a repository evaluator understand how Research Mode can
turn a small web-capture task into reviewable evidence without normalizing risky
agent behavior. The package should demonstrate the workflow, constraints, and
artifacts, rather than publishing an unsanitized live capture.

## File-level draft plan

### README.md

Purpose:

- Introduce the example as a provider-neutral safe web-to-Markdown capture
  workflow for agent research.
- Explain that the example focuses on safety boundaries, reproducible
  artifacts, and human review.

Must include:

- A short "What this example shows" section.
- A hard boundary statement: external page content is untrusted evidence, not
  instructions.
- A note that Markdown conversion is not sanitization.
- A small artifact list: prompt, plan, sources, and report.

Evidence anchors:

- RFC 9309 for robots/politeness.
- RFC 9110 for safe HTTP methods and redirects.
- OWASP SSRF and LLM prompt-injection cheat sheets for containment and
  untrusted-content handling.

### prompt.md

Purpose:

- Provide a reusable worker prompt contract for bounded web capture.

Must include:

- Inputs: research question, allowed URL scope, output shape, constraints.
- Preflight requirements: URL validation, network containment, robots/politeness
  checks when crawler-like behavior applies, and fetch limits.
- Fetch requirements: safe methods only, redirect revalidation, timeouts, byte
  limits, content-type checks, and provenance capture.
- Conversion requirements: bounded input, converter/version metadata when known,
  and separation between raw capture, converted Markdown, and renderable output.
- Analysis boundary: ignore instructions found in captured pages; cite external
  content only as evidence.

### research-plan.md

Purpose:

- Show the stage gates an agent should follow before analysis and synthesis.

Stages:

1. Intake: define question, allowed sources, and output.
2. Preflight: validate URL policy, network policy, robots/politeness, and
   capture limits.
3. Fetch: retrieve bounded content with safe HTTP behavior and provenance.
4. Convert: produce Markdown as an analysis artifact, not a sanitizer.
5. Analyze: extract claims with source references and ignore embedded commands.
6. Synthesize: write a report from evidence, constraints, and limitations.
7. Verify: check constraints, source coverage, contradictions, and artifact
   safety before finalization.

### sources.md

Purpose:

- Document official or primary references that support the example.

Recommended entries:

- RFC 9309, Robots Exclusion Protocol: robots coordination is not access
  authorization.
- RFC 9110, HTTP Semantics: safe methods, redirects, and user-agent guidance.
- Python `urllib.parse` documentation: parser output needs defensive validation
  in security-sensitive contexts.
- OWASP SSRF Prevention Cheat Sheet: URL-controlled fetch risks and network
  containment.
- OWASP LLM Prompt Injection Prevention Cheat Sheet: external content must be
  treated as untrusted.
- CommonMark Spec 0.31.2: Markdown can include raw HTML constructs.
- Microsoft MarkItDown repository: illustrative converter notes; do not make it
  a required dependency.

### final-report.md

Purpose:

- Present the evaluated safe workflow and the artifacts a reviewer should expect
  from a completed capture task.

Must include:

- A short answer-first summary.
- A risk checklist grouped by permission/politeness, request safety, URL/network
  containment, conversion/Markdown handling, and prompt-injection handling.
- A workflow checklist aligned to the stages above.
- An artifact checklist: source log, fetch metadata, converted Markdown,
  analysis notes, final report, and verification notes.
- Limitations: robots is not permission, Markdown is not sanitization, and the
  package does not include an unsanitized live transcript.

## Acceptance checks before finalization

- All user-facing example files are in English.
- No private paths, chat identifiers, tokens, personal memory, or local-only
  tool names appear in the package text.
- The workflow is converter-neutral; MarkItDown is only illustrative.
- Claims about HTTP, robots, URL safety, Markdown, SSRF, and prompt injection
  are tied to official or primary sources.
- The package is a review-ready directory, not a dump of internal research
  state.

