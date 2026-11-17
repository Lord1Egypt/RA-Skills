## Description:

Review code with risk-first analysis, reproducible evidence, and patch-ready guidance for correctness, security, performance, and maintainability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to review code, pull requests, and merge readiness with risk-ranked findings, reproducible evidence, concrete fix paths, and required test coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local review memory may retain sensitive project context if the user approves saving it.

Mitigation: Confirm planned writes before creating or updating ~/review-code/ and do not save secrets, credentials, private code snippets, or sensitive payloads.

Risk: Review output can be misleading if findings are applied outside the requested scope or without reproducible evidence.

Mitigation: Keep review scope explicit, tie findings to concrete evidence and impact, and treat low-confidence issues as questions or required verification steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/review-code)
- [Skill Homepage](https://clawic.com/skills/review-code)
- [Setup](setup.md)
- [Review Workflow](review-workflow.md)
- [Severity and Confidence Guide](severity-and-confidence.md)
- [Language and Architecture Risk Checklists](language-risk-checklists.md)
- [Test Impact Playbook](test-impact-playbook.md)
- [Patch Strategy for Review Findings](patch-strategy.md)
- [Review Comment Templates](comment-templates.md)
- [Memory Template](memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or plain text with optional code snippets and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk-ranked findings include severity, confidence, evidence, impact, fix direction, test gaps, residual risks, and merge recommendation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
