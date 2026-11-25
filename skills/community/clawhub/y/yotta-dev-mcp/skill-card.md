## Description:

A local stdio MCP server that gives coding agents deterministic tools for mapping repositories, reviewing architecture and changes, tracking verification evidence, and checking code, dependencies, secrets, and release readiness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use it through an MCP client to understand unfamiliar repositories, assess architecture and change impact, and produce evidence-backed review and verification reports. Execution and write actions are opt-in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious, citing purpose and behavior mismatches, unpinned package launch examples, partial component inspection, and a degraded static tool-misuse analyzer.

Mitigation: Review the package source and its configuration discovery and installer changes before installing. Treat the scan as incomplete because not all components were fully inspected and the static analyzer was degraded.

Risk: Explicit options can run project checks or adapters and can write scaffold or workflow state.

Mitigation: Enable execution or apply options only for a reviewed repository and an intended operation; otherwise leave the default gates closed.

## Reference(s):

- [ClawHub release](https://clawhub.ai/yottameta/skills/yotta-dev-mcp)
- [Project homepage](https://github.com/YottaMeta/yotta-dev-mcp)
- [Tool reference](references/tools.md)
- [Architecture contract reference](references/architecture-contract.md)
- [Optional adapters reference](references/adapters.md)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [Structured JSON tool results with evidence-linked summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes file and line evidence, rule findings, and explicit UNKNOWN states when inputs, configuration, or tools are insufficient.]

## Skill Version(s):

0.2.9 (source: frontmatter, CHANGELOG, package.json; released 2026-11-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
