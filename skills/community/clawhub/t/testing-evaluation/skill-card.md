## Description:

Design eval test cases, run regression tests, and generate quality reports for AI Agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QA engineers use this skill to design evaluation cases, run manual or automated regression checks, and produce quality reports for AI agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation reports, reproduction steps, commits, or tracker issues may expose sensitive prompts, outputs, credentials, personal data, or raw transcripts.

Mitigation: Choose commit and issue destinations explicitly, and redact secrets, credentials, private prompts, personal data, and raw transcripts before publishing artifacts.

Risk: Generated evaluation artifacts or recommendations may be incorrect or misleading if accepted without review.

Mitigation: Review and scan test cases, scripts, reports, and recommendations before deployment or use in release decisions.

## Reference(s):

- [Testing Evaluation ClawHub Page](https://clawhub.ai/bettermen/skills/testing-evaluation)
- [测试用例模板](references/eval-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with optional JSON and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local Markdown evaluation reports, test-case definitions, or connector-bound Git and issue-tracker updates when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
