# Capability detection

Use this checklist before the SEO/GEO workflow. It is deliberately runtime-neutral
so Hermes Agent, OpenClaw, and other loaders can provide different adapters.

| Capability | Required properties | If unavailable |
| --- | --- | --- |
| Search/query | declared, read-only, scoped, returns source URLs | use supplied sources or record a data gap |
| Supplied documents | user-provided or runtime-declared, bounded, read-only | do not obtain outside material; record a data gap |
| Analytics/visibility data | explicitly authorized read-only scope, redacted output | do not request credentials; mark unavailable |
| Competitor registry | local, supplied, or declared read-only source | ask for a source or return `SKIP` |
| Artifact rendering | local in-memory/response formatting only | return the contract as text |

For every capability used, record its name, availability, read-only status,
scope/limits, and an evidence reference. A tool is not approved merely because
it is present: reject capabilities that can publish, mutate, send, or access
secrets unless the current task is strictly read-only and the mutating mode is
not invoked.

Never probe for credentials, install a dependency to bypass a missing adapter,
execute shell/scripts, or add telemetry. A capability failure is an explicit
limitation, not permission to widen the boundary.
