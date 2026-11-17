## Description:

Used to capture and organize notes, ideas, quotes, and journal entries with automatic tagging, linking, and knowledge graph maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jrswab](https://clawhub.ai/user/jrswab)

### License/Terms of Use:


## Use Case:

External users and developers use SlipBot to capture prefixed notes, ideas, quotes, and journal entries into a local slipbox, then maintain tags, source metadata, bidirectional links, and a JSON graph for later retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad prefix-based auto-capture can write local notes and graph updates when ordinary Markdown-like messages are entered.

Mitigation: Use the skill only where note capture is intended, or require an explicit capture command or confirmation before writing files.

Risk: The skill may inspect USER.md or system context to determine timezone.

Mitigation: Provide timezone explicitly or restrict access to personal user-profile files unless that access is deliberate.

Risk: Broken-link cleanup and graph rebuilding can modify existing slipbox metadata.

Mitigation: Keep the slipbox under version control or backup before enabling automated cleanup and graph updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jrswab/skills/slipbot)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown note files, JSON graph updates, and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates persistent files under slipbox/ when capture patterns match.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
