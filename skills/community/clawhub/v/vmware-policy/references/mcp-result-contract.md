# Shared MCP result contract (Policy 1.26.0)

This is a library/transport contract, not a new MCP tool or a permission grant.
Existing tool names, arguments, success values and CLI prompts are unchanged.

## Errors

For a failed MCP tool result, `isError` remains true. Clients can read the
same structured view across legacy string, object and one-row-list errors:

```json
{"structuredContent":{"vmware_error":{"error":"Resource not found","hint":"List resources first"}},"isError":true}
```

`error` is a nonempty string. `hint` is an authored string or null, not a guessed
remedy. `vmware_error` is reserved transport metadata. Existing text content and
structured business fields are retained, so clients can migrate their parser
without changing Python tool callers. Clients reading only `content` continue
to see legacy error shapes; they must consume the structured view to use this
common contract. Migrating the text body itself needs a separately versioned change. Successes, previews and recovered nested
failures do not acquire an error view merely because their data mentions errors.
SDK ToolError messages keep their existing text and receive the same view;
cancellation is propagated. This does not add an error-code taxonomy or relax
Policy/RBAC, audit, undo, circuit or confirmation checks.

The full structured object gains a field on failure: clients comparing entire
objects for equality must allow that documented additive field. Read the common
view or the legacy text as appropriate; displaying both can duplicate diagnostics.

## Offset pages

`page_envelope` retains `items`, `returned`, `limit`, `total`, `truncated`, `hint`
and adds `offset` and `next_offset` for tools that actually support offsets.
Stop when `next_offset` is null; do not loop on `truncated`. Unknown totals stay
null, and a full last page with an unknown total can require an empty read.
Empty pages terminate. Domain-specific page caps/defaults remain with each skill.

The new helper defines `truncated` as “this page is not the entire collection.”
Legacy helpers including AIops, Harden, Storage and VDI/PrivateAI temporarily retain their older “more pages remain”
meaning and hint values while adding the shared `next_offset`. Their old fields
are not silently redefined. Use `next_offset` in portable clients. Tools with no
offset argument do not gain a fabricated continuation; cursor APIs keep cursors.

Deployment order: release Policy 1.26.0 first, then update dependent skills and
regenerate their release locks. Source-overlay tests are not a released rollout.
