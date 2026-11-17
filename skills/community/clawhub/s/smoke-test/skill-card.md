## Description:

Multi-modal LLM-assisted workflow for testing, fixing, regression-verifying, and reporting on web application quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xburn747](https://clawhub.ai/user/xburn747)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and QA engineers use this skill to run systematic web application smoke and regression testing, compare UI behavior with backend truth, guide code-level fixes, and produce evidence-chain reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can lead an agent toward destructive tests, production uploads, database restores, SSH actions, service restarts, or persistent memory updates.

Mitigation: Use it only on systems the user owns or is authorized to test, prefer read-only or staging environments, and require separate confirmation before write, deletion, production, restore, SSH, restart, or memory-update actions.

Risk: Reports and captured application text may contain secrets, personal data, or untrusted content from the tested application.

Mitigation: Use scoped test credentials and review generated reports, screenshots, and persisted notes before publishing or storing them.

## Reference(s):

- [Verification Schemes V1-V11](references/verification-schemes.md)
- [Smoke Test ClawHub Skill Page](https://clawhub.ai/xburn747/skills/smoke-test)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JavaScript templates, shell commands, JSON test summaries, screenshots, and self-contained HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce test artifacts such as smoke_result.json and screenshots when the included templates are run.]

## Skill Version(s):

1.0.0 (source: frontmatter, metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
