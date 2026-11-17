## Description:

Skill Validator checks ClawHub skill packages for required files, metadata, shell script syntax, permissions, and format issues, then reports problems and repair guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill publishers use Skill Validator to preflight ClawHub skills before release by checking package structure, metadata, script syntax, permissions, and compatibility issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary flags the skill as suspicious because its documentation encourages unpinned remote publishing scripts and higher-impact publish workflows.

Mitigation: Review before installing; avoid curl-and-run flows unless pinned to a reviewed commit with a verified checksum, and use publish or CI examples only with intentionally scoped credentials.

Risk: The installer can create or replace global command links under /usr/local/bin when run with --link.

Mitigation: Run install.sh without --link unless global command replacement is intended, and review the target paths and permissions first.

Risk: Validation and repair guidance can affect release decisions or local skill files.

Mitigation: Treat reported fixes as recommendations; review and scan the skill before deployment or publication.

## Reference(s):

- [Skill Validator on ClawHub](https://clawhub.ai/puppetcat-fire/skills/skill-validator)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [OpenClaw Skill Development Guide](https://github.com/openclaw/openclaw/docs/skills.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Terminal output with optional JSON validation reports and Markdown-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash, jq, find, grep, and sed according to the release metadata.]

## Skill Version(s):

1.0.11 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
