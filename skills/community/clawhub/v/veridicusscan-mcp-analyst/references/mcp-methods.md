# VeridicusScan MCP methods

This reference supports the `veridicusscan-mcp-analyst` skill.

## Session lifecycle

- `health`
- `list_methods`
- `open_session`
- `close_session`

Open a session before scan or runtime-defense operations. Close it when the task is complete.

Operational constraints:

- The bridge allows one active session at a time.
- `scan_url` accepts only public HTTPS destinations.
- Bare hosts such as `www.cnn.com` may be normalized to `https://...` before validation.
- Blocked internal destinations surface `error.code = "non_public_network_url"`.

## Scan methods

- `scan_text`
- `scan_url`
- `scan_file`
- `get_report`
- `export_report`

Use the narrowest scan surface first. Prefer `scan_text` for a prompt or snippet, `scan_file` for a local artifact, and `scan_url` for a live web target.

When summarizing scan results, include:

- `risk_band`
- `risk_score`
- `default_context_mode` when present
- `total_findings`
- top findings and evidence preview
- coverage notes, especially partial-scan reasons

If `default_context_mode = "sanitized_only"`, prefer `safe_context` for downstream use. Treat inline report surfaces as redacted by default.

## Runtime-defense methods

- `ingest_memory`
- `retrieve_memory`
- `selective_disclosure`
- `evaluate_selective_disclosure`
- `scope_tools`
- `guard_plan`
- `gate_action`

### Safe ordering

1. `open_session`
2. `scope_tools`
3. `guard_plan`
4. `gate_action`
5. `close_session`

For memory or disclosure tasks:

1. `open_session`
2. `ingest_memory`
3. `retrieve_memory` or `selective_disclosure`
4. `evaluate_selective_disclosure` if the user wants quality verification
5. `close_session`

## Triage guidance

- A high hidden-style or obscured-text signal alone is not enough to call a page malicious.
- Partial coverage matters. Explain whether the fetch was capped, the artifacts were chunked, or a file type limited extraction.
- If the evidence is code-like, config-like, or clearly infrastructural, say that it may be a false positive.
- Distinguish structural findings from semantic intent findings.
- When a URL is blocked as non-public, explain that this is an intentional SSRF boundary, not a transient network failure.

## Local bridge note

If you bundle this skill with the VeridicusScan source tree, keep a local protocol note alongside it. The published skill itself should stay portable and avoid repo-local absolute paths.
