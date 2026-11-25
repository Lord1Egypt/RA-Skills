## Description:

An audit-first workflow that helps developers sanitize, verify, and publish OpenClaw skills to ClawHub, SkillHub, and GitHub while protecting private data and credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haiyangchenbj](https://clawhub.ai/user/haiyangchenbj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to prepare OpenClaw skills for release by auditing and sanitizing content, checking the staged files, and guiding an approval-based publish and install check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags an approval gap in a publishing helper and concerns about network permissions.

Mitigation: Review the publishing steps and declared permissions, and require explicit approval before any public upload.

Risk: The security scan was partial; some instruction text and references were not fully evaluated.

Mitigation: Review the remaining components and references before installing or invoking publishing features.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/haiyangchenbj/skills/skill-audit-publish)
- [Publish rules for ClawHub and GitHub](references/publish-rules.md)
- [SkillHub publishing guide](references/skillhub-publish.md)
- [GitHub sync helper](scripts/sync_skill_to_github.js)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files, Shell commands, Code, Configuration guidance]

**Output Format:** [Markdown checklists and approval summaries, with shell commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a sanitized staging folder, file manifest, and reviewable publish details.]

## Skill Version(s):

1.5.13 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
