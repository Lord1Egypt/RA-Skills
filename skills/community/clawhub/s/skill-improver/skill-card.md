## Description:

Reviews and improves OpenClaw SKILL.md files against defined quality criteria and grading guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phallusophy](https://clawhub.ai/user/phallusophy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to audit OpenClaw SKILL.md files, receive an A-D quality grade, and get targeted remediation guidance or an optimized SKILL.md when issues are found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read a user-provided SKILL.md path during review.

Mitigation: Review only intended skill files and avoid pointing the agent at unrelated sensitive files.

Risk: Suggested optimized SKILL.md content could be incorrect or unsuitable for a specific project's standards.

Mitigation: Review proposed changes before applying them and keep a backup of the original skill file.

Risk: Malformed, missing, or empty skill files can prevent a successful review.

Mitigation: Check the file path and SKILL.md structure, then use the documented parse, missing-file, or empty-content failure handling.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phallusophy/skills/skill-improver)
- [OpenClaw Skill Quality Tools](artifact/SKILL.md)
- [OpenClaw Skill Quality Standard](artifact/skill-standard/skill-standard.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, JSON, Guidance]

**Output Format:** [Markdown review report with optional optimized SKILL.md and JSON status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include quality grade, issue and warning counts, dimension scores, remediation suggestions, and failure codes for parse or file errors.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
