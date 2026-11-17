## Description:

OpenClaw Skill template generator that creates skill scaffolds, validates structure, enhances SKILL.md, generates command frameworks and tips, and prepares publish checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to scaffold OpenClaw skills, validate skill structure, generate command frameworks and tips, and prepare publish checklists. It can also act as a simple local text logging CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local entries and command arguments can be retained in plaintext history and data logs.

Mitigation: Do not enter secrets or sensitive business data; set SKILL_TEMPLATE_DIR to a reviewed location and clear logs before sharing or packaging outputs.

Risk: Generated templates can include fixed promotional branding that may not fit the downstream skill owner or release context.

Mitigation: Review generated scaffold text and remove or replace promotional footer content before publishing a derived skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ckchzh/skills/skill-template)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell and Python code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated scaffold and data-log commands may write local plaintext files.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
