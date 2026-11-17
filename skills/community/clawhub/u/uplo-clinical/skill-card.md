## Description:

Uplo Clinical provides AI-powered clinical operations intelligence spanning pharmaceutical development and healthcare delivery with unified search across clinical trials, protocols, and patient care documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roojenkins](https://clawhub.ai/user/roojenkins)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical operations, pharmaceutical, healthcare, and regulatory teams use this skill to search organization-specific clinical trial protocols, patient care documentation, formulary materials, adverse event records, and operational SOPs through UPLO-backed MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts an unpinned MCP package while using an API token.

Mitigation: Verify the @agentdocs1/mcp-server package provenance before installation and pin or otherwise control the exact version that runs.

Risk: Identity, directive, export, and clinical search tools can expose sensitive organizational or clinical context.

Mitigation: Use a least-privilege UPLO token, restrict export and directive tools to authorized users, and retrieve identity or directives only when needed for the task.

Risk: Clinical trial data and patient health information may be highly sensitive and can be misapplied if context is mixed or fabricated.

Mitigation: Respect classification tiers, distinguish investigational from approved therapies, keep individual patient data separate from aggregate research findings, and surface only information present in the knowledge base.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/roojenkins/skills/uplo-clinical)
- [UPLO](https://uplo.ai)
- [UPLO Schemas](https://uplo.ai/schemas)
- [README](artifact/README.md)
- [Identity Patch](artifact/identity-patch.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell and tool-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured UPLO instance URL and API token; tool results are governed by the connected organization's access controls.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
