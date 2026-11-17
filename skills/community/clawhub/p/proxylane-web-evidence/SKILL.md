---
name: proxylane-web-evidence
version: 1.0.0
description: >-
  Collect bounded, traceable web observations through a supplied ProxyLane HTTP
  connection: YouTube caption segments or comments, Google AI citations,
  Xiaohongshu notes through an existing MCP session, and identified product offers.
  Use for source collection and access diagnostics before RAG, voice-of-customer
  analysis, citation comparisons or price monitoring. Requires explicit source
  identity and records coverage; does not promise universal site access.
triggers:
  - "collect verifiable web evidence with ProxyLane"
  - "fetch YouTube transcripts through my proxy for RAG"
  - "collect a bounded YouTube comments sample with source links"
  - "capture Google AI citations for a regional comparison"
  - "collect Xiaohongshu note evidence through my existing MCP"
  - "observe this identified product price through ProxyLane"
tools:
  - exec
  - read
  - write
mutating: true
eval_contract:
  goal: |
    Give an agent repeatable source observations with matching target identity,
    redacted raw evidence and honest access/coverage outcomes using a supported
    supplied ProxyLane connection. Excellent output lets another operator trace
    each observation to the captured input without confusing fixtures, samples,
    provider declarations or regional assumptions with live verified facts.
  dimensions:
    - "SOURCE_IDENTITY — do captions, comments, notes and offers match the requested source and required semantic fields?"
    - "TRACEABILITY — can every observation be checked against dated, hashed, redacted input evidence and source links?"
    - "ACCESS_DIAGNOSIS — are challenges, missing captions/session, unsupported DOM and dependency failures distinguished with bounded next steps?"
    - "COVERAGE_HONESTY — are sampling, pagination, regional uncertainty, variants and checkout limitations stated in machine-readable output?"
    - "EXECUTABILITY — can the documented source commands run in an isolated runtime without hidden services or deployment assumptions?"
    - "CREDENTIAL_BOUNDARY — are credentials absent from outcomes, persisted evidence and yt-dlp command arguments?"
  hard_fails:
    - "Presenting synthetic fixtures, HTTP success, proxy declarations or an unrelated page as live source proof."
    - "Persisting or printing proxy credentials, cookies, API keys, MCP authentication tokens or xsec tokens."
    - "Treating organic links as AI citations, or gl/hl/exit IP alone as verified regional visibility."
    - "Publishing a comment, changing an account/session, installing a server, or making a paid managed-API call as an implicit fallback."
    - "Inventing missing captions, prices, currencies, variant identity, social comments or OCR content."
---

# ProxyLane Web Evidence

## Contract

One capability, five source modes: collect verifiable observations using a supplied [ProxyLane](https://proxylane.dev) connection before an agent analyzes or recommends anything. Source modes share a JSON outcome contract, deterministic normalization, credential redaction, raw-input hashes and a total deadline. Analysis, RAG indexing, representativeness and commercial conclusions are downstream work.

This release accepts a supplied HTTP/HTTPS proxy URL with an explicit port from `PROXYLANE_PROXY_URL` or a private one-line `--proxy-file`. No credentials are arguments. Xiaohongshu instead requires `XHS_PROXY` already configured on the existing server; the client can record that declaration but cannot prove or change server egress. Provider provenance is user supplied. A proxy can be blocked and does not provide login, missing content, authorization, stable IP retention or universal access.

The closest existing capabilities are proxy setup, general web research, video summarization and data research. Use those for connection provisioning, discovery/synthesis, or Brain ingestion. This skill remains separate because it owns source-specific identity checks, bounded raw observations and portable evidence outcomes, and does not replace their workflows. Manifest/resolver overlap was reviewed before creation; publishing must add routing entries at their owner, not a vendor cache.

## Phases

1. **Choose a mode and the semantic target.** Read [source modes](references/source-modes.md). A video needs its id and caption language; a note needs id/xsecToken or a search query; a price needs SKU/ASIN and optional variant. Google needs a reviewed, current AI surface DOM contract. Do not convert a search result or login page into a successful target observation.
2. **Prepare the isolated runtime and approved connection.** Follow [running](references/running.md). Reuse a supplied approved secret through the runtime environment; do not copy it into examples, the skill directory, prompts, command arguments or artifacts. Check executable/dependency versions. Never install into application dependencies.
3. **Run a fixture demonstration first when evaluating the skill.** `python3 scripts/collect.py --mode demo --fixture --out output/fixture-demo`. This calls all five normalization pipelines with explicitly synthetic inputs. It validates local execution, not target access, browser selectors, live captions, sessions or proxy reliability.
4. **Run one explicit live collection.** Use the mode command in [running](references/running.md), retain the JSON outcome and raw evidence. Optional `--verify-egress` performs a separate HTTP exit-IP probe; it cannot prove the target request's IP or country. A browser and an API may see different IPs on a rotating connection.
5. **Interpret status and coverage before analysis.** Read [output contract](references/output-contract.md). `partial` can contain useful real observations with incomplete or unverified context. `blocked`, `no_data`, `missing_session` and `unsupported_surface` require different remedies. Do not retry a login/CAPTCHA indefinitely or silently substitute a managed provider.
6. **Deliver evidence with its limits.** Cite source URLs, observation time, mode, proof_mode, coverage, diagnostics and artifact hashes. Separate observed content from analysis. Compare regions or repeat prices only after controlling the relevant language, surface, session, product variant and delivery context. Regional causality and checkout totals remain outside this collector's guarantees.

## Output Format

The CLI emits JSON on stdout and, when `--out` is supplied, saves `outcome.json` and selected redacted raw input files. Observations include timestamped caption segments, comment ids/links, a visible cited AI answer, a matching XHS note, or an identified offer. See the [field contract](references/output-contract.md) and [synthetic representative output](examples/fixture-output.json).

The .mjs entrypoint delegates to Python for runtimes that expect a JavaScript skill script: `node scripts/proxylane-web-evidence.mjs --mode demo --fixture`. Set `PROXYLANE_EVIDENCE_PYTHON` to an isolated interpreter when needed. POSIX process-group deadlines bound source subprocesses and browser descendants.

## Release Verification

[Verification boundaries](references/verification.md) and [KNOWN_GAPS](references/KNOWN_GAPS.md) distinguish executed checks from unproven coverage. The first-release cross-modal gate was explicitly waived after an inconclusive attempt; no authoritative PASS is claimed. Local unit/integration and proposed routing tests are runnable with `python3 -m unittest discover -s tests -v`. Global resolver registration and publication receipts belong to the release owner. Do not describe this candidate as published or production validated before its actual delivery receipts exist.
