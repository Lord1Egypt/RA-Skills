## Description:

Distill a simp dog into an AI Skill. Import WeChat history, generate Simping Memory + Persona, with continuous evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brother-yang](https://clawhub.ai/user/brother-yang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create local roleplay/persona agent skills from chat logs, screenshots, social posts, or pasted memories. It guides intake, analyzes memory and persona patterns, previews the result, and writes generated skill files for continued local use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read private chats, screenshots, photos, and other relationship data.

Mitigation: Use only data you have permission to process and redact names, locations, contact details, and other identifying information before import.

Risk: Generated skills persist as local agent instructions and may preserve sensitive or unhealthy relationship patterns.

Mitigation: Review every generated SKILL.md before activation, keep generated files scoped to a deliberate slug and output path, and delete or roll back generated instances that are no longer needed.

Risk: Roleplay output could be misused for impersonation, harassment, monitoring, or pressuring real people.

Mitigation: Use the skill only for consensual entertainment or personal reflection, and do not use generated personas to contact, pressure, or represent real people.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/brother-yang/skills/simp-dog-skill)
- [Publisher profile](https://clawhub.ai/user/brother-yang)
- [README_EN.md](artifact/README_EN.md)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated local files and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates local memory, persona, metadata, and SKILL.md files under a per-character simps/{slug}/ directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
