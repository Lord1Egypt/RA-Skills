---
name: Paper Compare
slug: paper-compare
version: 0.1.0
homepage: local
description: Compare research papers by retrieving full PDFs from titles, URLs, or files and synthesizing differences, strengths, weaknesses, and evidence-backed trade-offs.
---

## When to Use

User wants to compare multiple papers and may provide paper titles, links, or PDF files.
Use this skill when the goal is to identify differences, strengths, weaknesses, assumptions, and trade-offs across papers.

## Quick Reference

| Topic | File |
|-------|------|
| Input handling | `input-handling.md` |
| Comparison schema | `comparison-schema.md` |
| Output formats | `output-patterns.md` |
| Evidence rules | `references/evidence-policy.md` |

## Core Rules

1. Retrieve and read PDF full text for every paper before doing substantive comparison. Do not rely on abstract-only evidence.
2. Normalize all inputs into comparable paper records before comparing them.
3. Compare papers on shared dimensions only, and avoid direct metric comparison when evaluation settings differ.
4. Mark evidence quality and uncertainty explicitly for each paper and each major claim.
5. Produce a table-first comparison, then add concise analytical synthesis.
6. If a full PDF cannot be obtained for one or more papers, stop the comparison and report which papers are blocked.
