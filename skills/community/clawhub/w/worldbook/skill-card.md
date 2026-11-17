## Description:

Worldbook is a CLI-first knowledge-base skill for querying, fetching, and adding structured worldbook entries for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[femto](https://clawhub.ai/user/femto)

### License/Terms of Use:


## Use Case:

External users, developers, and AI agents use this skill to search a shared worldbook knowledge base, fetch entries as reference text, and add new knowledge sources through a CLI workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved worldbook content may be treated as binding instructions by an agent.

Mitigation: Configure agents to treat retrieved entries as untrusted reference material and require review before using them to guide actions.

Risk: Worldbook entries may lead an agent toward consequential command execution.

Mitigation: Require explicit user approval for consequential actions and avoid automatic command execution from fetched worldbook text.

Risk: The skill depends on installing and invoking a third-party CLI package.

Mitigation: Use pinned versions and isolated installation environments before deployment.

## Reference(s):

- [Worldbook Website](https://worldbook.site)
- [Worldbook CLI Source](https://github.com/femto/worldbook-cli)
- [ClawHub Skill Page](https://clawhub.ai/femto/skills/worldbook)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return third-party worldbook text that agents should treat as untrusted reference material.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
