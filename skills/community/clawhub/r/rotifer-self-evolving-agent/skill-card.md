## Description:

Ranks a project's Rotifer Genes against Arena data, recommends stronger alternatives, and can create Agent definitions or run local Agents when invoked with `/evolve`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoba-dev](https://clawhub.ai/user/xiaoba-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to assess local Rotifer capabilities against Arena rankings, review upgrade options, and manage project Agents. Upgrades and Agent creation require approval; `/evolve run-agent` executes the selected local Genes in a WASM sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence rates the skill benign with medium confidence and partial coverage; several path-like references were unresolved.

Mitigation: Review the pinned MCP package and any unresolved references before use; the skill documents installing the pinned package yourself before configuring it to run.

Risk: The documented MCP server makes network requests and has credential-handling behavior when the user is logged in.

Mitigation: Review the documented service requests and login-token handling, and use the documented telemetry opt-out if appropriate.

Risk: `/evolve run-agent` executes local Gene code, although the skill says it remains in the WASM sandbox.

Mitigation: Run only Agents you intend to execute and keep the sandbox enabled.

## Reference(s):

- [Rotifer Documentation](https://rotifer.dev/docs)
- [Rotifer Protocol](https://rotifer.dev)
- [Rotifer Capability Marketplace](https://rotifer.ai)
- [MCP Server v0.20.2 on npm](https://www.npmjs.com/package/@rotifer/mcp-server/v/0.20.2)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Configuration files, Code]

**Output Format:** [Text reports and project files (Agent definitions and Genes)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are presented as text; approved upgrades and Agent creation write project files, and run-agent executes Genes in a WASM sandbox.]

## Skill Version(s):

2.4.18 (source: SKILL.md frontmatter, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
