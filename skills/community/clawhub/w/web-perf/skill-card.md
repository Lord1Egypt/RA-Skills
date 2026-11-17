## Description:

Analyzes web performance using Chrome DevTools MCP, measuring Core Web Vitals and identifying render-blocking resources, network dependency chains, layout shifts, caching issues, and accessibility gaps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elithrar](https://clawhub.ai/user/elithrar)

### License/Terms of Use:


## Use Case:

Developers and engineers use Web Perf to audit page-load performance, Core Web Vitals, network behavior, and high-level accessibility gaps. It helps produce prioritized findings and concrete optimization recommendations for first-party codebases or externally audited sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path asks users to run a mutable third-party Chrome DevTools MCP package locally via npx without pinning a reviewed version.

Mitigation: Pin chrome-devtools-mcp to a reviewed version, avoid auto-confirming installs where practical, and run the MCP server with the least local and browser access needed for the audit.

Risk: Performance recommendations and code snippets can be misleading if based on incomplete traces, unavailable MCP tools, or unverified assumptions about unused assets.

Mitigation: Verify findings with Chrome DevTools MCP measurements, network requests, DOM state, and source code before applying changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elithrar/skills/web-perf)
- [Publisher profile](https://clawhub.ai/user/elithrar)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, prioritized findings, recommendations, code snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include measured Core Web Vitals, estimated impact, and codebase findings when source access is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
