## Description:

Monitor CVEs and security advisories through the Chinng AI-Agent Portal. Use for incremental vulnerability checks, package watchlists, and actionable security summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinng-inta](https://clawhub.ai/user/chinng-inta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to monitor watched packages, vendors, products, CVE IDs, and OSV IDs, then summarize relevant advisory changes with source attribution and affected-version evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security-advisory queries and watchlist-like package, vendor, or product names are sent to an external Chinng portal endpoint.

Mitigation: Use the skill only where sharing those queries with the portal operator is acceptable, and avoid submitting sensitive internal watchlists unless approved.

Risk: Vulnerability summaries may be incomplete or stale if portal records lag behind upstream advisory sources.

Mitigation: Validate important vulnerability claims against upstream advisory source links before acting on remediation guidance.

Risk: A first change-feed run without bounds can process the full available history.

Mitigation: Bound first-run or cursor-recovery change-feed queries by date and persist the new cursor only after successful processing.

## Reference(s):

- [Chinng AI-Agent Portal MCP endpoint](https://portal.chinng-lab-srv.dev/mcp)
- [ClawHub skill page](https://clawhub.ai/chinng-inta/skills/security-watch)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and advisory summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves advisory identifiers, affected-version evidence, attribution, source links, and cursor-handling guidance.]

## Skill Version(s):

0.2.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
