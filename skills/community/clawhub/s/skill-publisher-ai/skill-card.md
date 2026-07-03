## Description: <br>
Publishes and updates skills to GitHub and ClawHub with repository scaffolding, security audit, change detection, version bumping, and changelog generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to prepare, validate, version, and publish agent skills to GitHub and ClawHub. It supports both first-time releases and iterative updates with security review and changelog generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe credential handling may expose or reuse sensitive GitHub credentials. <br>
Mitigation: Remove hardcoded tokens and local paths before use, rotate any exposed token, and prefer gh CLI or a secure credential manager. <br>
Risk: External publishing behavior may affect the wrong repository, account, visibility setting, file set, or ClawHub slug if inputs are not confirmed. <br>
Mitigation: Confirm the target repository, account, visibility, files to upload, and ClawHub slug before running any publish or update workflow. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/edwardwason/skill-publisher-ai) <br>
- [Repo Structure Reference](references/repo-structure.md) <br>
- [Security Audit Reference](references/security-audit.md) <br>
- [Publish Procedures Reference](references/publish-procedures.md) <br>
- [Change Detection Reference](references/change-detection.md) <br>
- [Changelog Generation Reference](references/changelog-generation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline command examples and generated repository files or configuration.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation for target repository, account, visibility, ClawHub slug, and version changes before publishing.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and SKILL.md frontmatter, released 2026-06-11) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
