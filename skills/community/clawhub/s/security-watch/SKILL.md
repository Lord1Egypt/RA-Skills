---
name: security-watch
version: 0.2.1
license: MIT-0
description: Monitor CVEs and security advisories through the Chinng AI-Agent Portal. Use for incremental vulnerability checks, package watchlists, and actionable security summaries.
---

# Security watch

Use the `portal` MCP server declared by this plugin.

Standalone install (no plugin): register the read-only MCP endpoint first — `openclaw mcp add portal --transport http https://portal.chinng-lab-srv.dev/mcp`. Other MCP clients: <https://portal.chinng-lab-srv.dev/mcp>.

1. Search or list the security family for watched packages, vendors, products, and CVE or OSV identifiers.
2. For recurring runs, combine newly published records with the portal's change feed so revised advisories are not missed.
3. Retrieve details only for relevant records and preserve the advisory's identifiers, affected-version evidence, attribution, and source link.
4. Separate confirmed impact from inference. Do not extend affected version ranges beyond the advisory data.

## Separate upstream advisory text from portal annotations

Security bodies are the one family that carries real document text — impact, patches, workarounds, affected and fixed versions, and upstream references.

Report only what the upstream advisory states, and attribute affected and fixed versions to the advisory. A record's text may also include deployment-specific notes that are not part of the upstream advisory; these are out of scope. Do not quote them, do not report them as affected-version findings, and do not carry them into a citation pack or any other output.

If a record appears to contain deployment detail that does not belong on a redistributable record, raise it with the requester privately rather than reproducing it.

## First run of the change feed

The change feed starts from the beginning of history when called without a cursor. On a first run, or whenever the saved cursor is lost, bound the feed by date rather than calling it bare, then save the returned cursor.

Persist a new change cursor only after successful processing, and follow each record's license and reuse metadata.
