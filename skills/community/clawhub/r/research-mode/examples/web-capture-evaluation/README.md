# Safe Web-to-Markdown Capture

This example shows a provider-neutral workflow for capturing a public web page as Markdown during an agent research task. It is designed for repository evaluators who want to see the safety boundaries, review artifacts, and verification checks that should surround web capture.

## What This Example Shows

- How to frame external page content as untrusted evidence, not instructions.
- How to separate intake, preflight, fetch, conversion, analysis, synthesis, and verification.
- Which artifacts make a web-capture run reviewable: prompt, plan, source log, fetch metadata, converted Markdown, analysis notes, final report, and verification notes.
- Why Markdown conversion is not sanitization and should not be treated as render-safe HTML.

## Safety Boundary

Captured pages, converted Markdown, page titles, metadata, and links are all untrusted input. An agent may cite them as evidence after analysis, but must not follow instructions embedded in them, run tools because a page requested it, or treat converted Markdown as trusted output.

The workflow also treats robots.txt as a politeness and coordination signal, not as authorization to access or republish content. Public examples should avoid publishing unsanitized live captures unless redistribution is explicitly allowed or the content is synthetic.

## Package Files

- `prompt.md` defines the reusable worker contract.
- `research-plan.md` describes the gated workflow.
- `sources.md` lists the primary references behind the example.
- `final-report.md` presents the evaluated workflow, risk checklist, and expected artifacts.

## Evaluation Notes

A good implementation of this example should be able to show its URL policy decision, redirect handling, fetch limits, source metadata, conversion metadata, and final constraint checks. The example stays converter-neutral; a converter may be named in a real run, but the safety model should not depend on one specific tool.
