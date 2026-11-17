## Description:

Searches Wikipedia and Wikimedia Commons for public media assets, returning page matches, embedded media, file URLs, metadata, and licensing context through AgentPMT-hosted calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and content workflows use this skill to find public Wikimedia media, retrieve direct file URLs, and inspect description or license context before using assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional setup commands may install related AgentPMT skills through routes that are not pinned in the artifact.

Mitigation: Prefer reviewed ClawHub or OpenClaw installation routes when available and inspect the referenced setup skills before installing them.

Risk: AgentPMT calls may spend account credits.

Mitigation: Confirm the intended action, account route, and expected credit cost before repeated or automated calls.

Risk: Account secrets, wallet material, signatures, or payment headers could be exposed if pasted into prompts or logs.

Mitigation: Use the referenced setup skill for credential handling and keep secrets out of prompts, examples, transcripts, and logs.

Risk: The language parameter defaults to English when not supplied.

Mitigation: Set the language parameter explicitly whenever non-English Wikipedia results are required.

Risk: Media returned from Wikimedia projects can have file-specific license terms.

Mitigation: Check the returned file description page and license context before reusing or redistributing media.

## Reference(s):

- [Generated action schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/public-commons-media-search)
- [AgentPMT marketplace product page](https://www.agentpmt.com/marketplace/public-commons-media-search)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration instructions, JSON]

**Output Format:** [Markdown instructions with JSON request examples and JSON tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote calls return Wikimedia titles, media lists, file URLs, metadata, snippets, pagination offsets, and licensing context; individual actions cost AgentPMT credits.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
