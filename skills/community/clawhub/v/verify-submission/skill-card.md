## Description:

Review OpenAnt applications and task submissions, including applicant decisions, file downloads, approval or rejection, and feedback on deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ant-1984](https://clawhub.ai/user/ant-1984)

### License/Terms of Use:

MIT-0

## Use Case:

Task creators and designated verifiers use this skill to review OpenAnt applicants and submitted work. It guides agents through checking submission details, downloading files, approving or rejecting deliverables, and giving worker feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving or rejecting submissions can release escrow, return work for revision, or move a task into dispute.

Mitigation: Require clear review instructions, compare work against the task criteria, and confirm task state before retrying final actions.

Risk: The skill uses an unpinned @openant-ai/cli@latest runtime, so command behavior can change between reviews.

Mitigation: Use a pinned and vetted OpenAnt CLI version in constrained environments.

Risk: Downloaded submission files may be untrusted or contain sensitive data.

Mitigation: Inspect files read-only unless sandboxed and approved, do not execute untrusted content, and limit PII handling to what the review requires.

## Reference(s):

- [Task Review Workflow](artifact/references/review-workflow.md)
- [Risk Warnings for Task Verification](artifact/references/risk-warnings.md)
- [Skills Ecosystem for Task Verification](artifact/references/skills-ecosystem.md)
- [ClawHub Skill Page](https://clawhub.ai/ant-1984/skills/verify-submission)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown guidance with bash command examples and JSON-oriented CLI instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenAnt CLI commands with --json and may download submission files for review.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
