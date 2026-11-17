## Description:

Generates production-oriented n8n workflow JSON from a user's automation requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yesong-hue](https://clawhub.ai/user/yesong-hue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation builders use this skill to turn clear n8n automation requirements into workflow JSON that can be reviewed, configured, and imported into n8n.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated n8n workflows may call APIs, use credentials, or change external systems depending on the user's prompt.

Mitigation: Review each generated workflow before importing or running it in n8n, especially credential use, external calls, and write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yesong-hue/skills/qnit-n8n-workflow)
- [Skill source](artifact/skill.md)
- [README](artifact/readme.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Configuration]

**Output Format:** [Markdown or text containing n8n workflow JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workflows should be reviewed before import or execution.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
