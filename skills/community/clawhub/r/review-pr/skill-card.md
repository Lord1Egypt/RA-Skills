## Description:

Reviews a GitHub pull request, reconciles prior review feedback, posts one consolidated PR comment, and monitors for the author's response until blocking issues are cleared.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunjeetsingh](https://clawhub.ai/user/arunjeetsingh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and code reviewers use this skill to run a repeatable PR review loop that checks current pull request changes against prior feedback and watches for an author response before re-reviewing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent monitoring can continue using the reviewer's GitHub authentication after the initial invocation.

Mitigation: Use narrowly scoped GitHub credentials where possible and confirm how to list, pause, or stop the host's watch before invoking the skill.

Risk: The skill can post follow-up PR comments as the authenticated reviewer during later review cycles.

Mitigation: Use it only for pull requests where unattended follow-up comments are intended, and stop the watch when monitoring is no longer needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/arunjeetsingh/skills/review-pr)
- [Publisher Profile](https://clawhub.ai/user/arunjeetsingh)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown PR review comments with concise status handoff text and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post one top-level GitHub PR comment per completed review cycle and may create or reactivate a background watch.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
