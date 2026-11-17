## Description:

Web and news search powered by Brave Search for agents that need current information, with pay-per-call Vincent credits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glitch003](https://clawhub.ai/user/glitch003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to let agents run web and news searches, return current result data, and track per-call Vincent credit usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill invokes the Vincent CLI at runtime using an unpinned latest package reference.

Mitigation: Pin or preinstall a reviewed Vincent CLI version before enabling the skill.

Risk: The skill supports wallet-funded credit purchases and an auto-replenish pattern.

Mitigation: Require human approval, strict external spend limits, and no exposed agent wallet unless autonomous top-up is explicitly approved.

Risk: The skill stores a scoped DATA_SOURCES credential in local configuration paths.

Mitigation: Protect the configured credential paths, keep search credentials separate from payment credentials, and revoke the key if access is no longer needed.

## Reference(s):

- [Vincent homepage](https://heyvincent.ai)
- [ClawHub skill page](https://clawhub.ai/glitch003/skills/vincent-brave-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON search result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses include result metadata and Vincent credit usage fields.]

## Skill Version(s):

1.0.69 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
