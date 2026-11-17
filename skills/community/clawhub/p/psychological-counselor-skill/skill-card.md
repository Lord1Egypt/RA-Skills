## Description:

Creates a psychological counselor AI skill from counselor background and consultation materials to support style simulation, professional learning, and bounded basic emotional support.

This skill is for research and development only.

## Publisher:

[zhuqingsonga](https://clawhub.ai/user/zhuqingsonga)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate a counselor-style agent from authorized, de-identified source material for learning, training, style simulation, and basic listening support. It is not intended to provide professional counseling, therapy, psychiatric diagnosis, crisis care, or replacement for licensed mental-health professionals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may process sensitive mental-health and counselor source material.

Mitigation: Use only fictional, authorized, public, or strongly de-identified material, and avoid entering private consultation records or personal data without clear permission.

Risk: Generated counselor agents could be mistaken for professional mental-health care or crisis support.

Mitigation: Keep the skill limited to learning, training, style simulation, and basic listening; direct users with crisis, diagnosis, therapy, or severe distress needs to qualified professionals or emergency resources.

Risk: Local delete, rollback, and update commands may affect more files than intended when counselor names or slugs are untrusted.

Mitigation: Review generated commands before execution and avoid delete or rollback operations with untrusted counselor names until slug and path validation are added.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhuqingsonga/skills/psychological-counselor-skill)
- [README](artifact/README.md)
- [Ethical Checklist](artifact/tools/ethical_checklist.md)
- [Quick Start](artifact/tools/quick_start.md)
- [Counselor Analyzer Prompt](artifact/prompts/counselor_analyzer.md)
- [Listening Support Prompt](artifact/prompts/listening_support.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON configuration, generated skill files, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local counselor skill directories, profile files, metadata, version archives, and prompt guidance after user confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
