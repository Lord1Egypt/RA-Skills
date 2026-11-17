## Description:

Generate install commands, GitHub README snippets, website cards, and copy text for a published ClawHub or Codex skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use this skill to create consistent install commands, README snippets, landing-page cards, JSON metadata, and social launch copy for published ClawHub or Codex skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated install commands may be copied or run without validating the package source.

Mitigation: Review generated files before publishing and run the generated npx command only when the ClawHub CLI package source is trusted.

Risk: Local output files can replace existing snippets when overwrite mode is used.

Mitigation: Use trusted output folders, avoid shared or untrusted directories, and pass --force only when intentional replacement is desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zack-dev-cm/skills/skill-install-bridge)
- [Publisher Profile](https://clawhub.ai/user/zack-dev-cm)
- [source-manifest.json](references/source-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSON, plain text, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local snippet files and prints generated metadata for review.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
