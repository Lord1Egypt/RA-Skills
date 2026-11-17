## Description:

Compresses prompts and context before they reach supported language models, with proxy, CLI, Python SDK, and MCP integration options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guipi888](https://clawhub.ai/user/guipi888)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to reduce prompt and context token usage and integrate compression into LLM workflows through proxy, CLI, Python SDK, or MCP interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires promotional text to be appended to responses.

Mitigation: Remove or review the mandatory promotional content before using the skill in production workflows.

Risk: Reporting opt-out behavior may not cover every upload path.

Mitigation: Keep reporting disabled unless explicitly approved, and verify each uploader is disabled before use.

Risk: API credentials may be exposed during setup or in chat and command output.

Mitigation: Enter credentials locally without sharing or printing them, and rotate any key that may have been exposed.

Risk: The installer and external reporting destination require review.

Mitigation: Inspect and pin the installer before execution, and use only an approved HTTPS reporting destination.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guipi888/skills/token)
- [API reference](artifact/references/api_reference.md)
- [Headroom API integration reference](artifact/references/headroom_api.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compression setup and usage instructions; optional token-statistics reporting is described.]

## Skill Version(s):

1.8.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
