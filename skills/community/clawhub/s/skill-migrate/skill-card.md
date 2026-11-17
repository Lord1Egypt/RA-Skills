## Description:

Skill Migrate helps agents convert WorkBuddy skill packages into OpenClaw/ClawHub-compatible skills, check required metadata and file constraints, and prepare ClawHub publishing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gongsunyanming](https://clawhub.ai/user/gongsunyanming)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to migrate WorkBuddy skills into OpenClaw/ClawHub format, validate publishing requirements, and prepare single-skill or batch releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Converted packages may copy and publish scripts or sensitive configuration files with too little review.

Mitigation: Review generated packages before publishing, especially scripts and configuration files, and remove secrets such as .env files or tokens.

Risk: Converted packages may use a fixed default author identity that does not match the intended publisher.

Mitigation: Confirm the author metadata, slug, version, and file list before allowing ClawHub publish to run.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gongsunyanming/skills/skill-migrate)
- [OpenClaw Skill Format Specification](artifact/references/openclaw-skill-spec.md)
- [OpenClaw Skill Format Documentation](https://docs.openclaw.ai/clawhub/skill-format)
- [ClawHub Text File Extensions Whitelist](artifact/references/text-file-extensions.txt)
- [WorkBuddy to OpenClaw Conversion Examples](artifact/references/conversion-examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce validation reports, converted SKILL.md content, supporting text files, and ClawHub publish commands.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
