---
name: quality_audit
description: Pre-dispatch and post-generation audits that catch parameter / asset / model-range / persona-flow issues before burning a worker round.
always_loaded: true
tool_names: []
---

# Quality audit

Pre-dispatch and post-generation audits that catch parameter, asset, model-range, and persona-flow issues before they burn a worker round. Findings come back as structured fatal/minor issues with a `recommended_action` (`accept` | `refine` | `regenerate` | `ask_user`).

This skill exposes no LLM-callable tools. The runtime invokes the audit between schema validation and tool execution; the result is surfaced as a tool-result envelope when the action is anything other than `accept`.

## Constraints

- When the audit returns `recommended_action="ask_user"`, surface the `fatal_issues` to the user and wait — do not retry the tool call.
- When `recommended_action="refine"`, apply the `fix_hint(s)` on the next attempt rather than repeating the same call.
