## Description:

Routes `/uv` requests by intent to a matching workflow skill for bug fixes, feature work, refactoring, or code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zengfr](https://clawhub.ai/user/zengfr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to route a `/uv` request to a bugfix, feature, refactor, or review workflow. It selects the default feature workflow when no intent is identified or intents conflict.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented route command uses `npx tsx`, which may download and run an unpinned package; the scan also could not resolve several local references.

Mitigation: Review the command before use, confirm the referenced files, and prefer a locally installed, lockfile-pinned `tsx` dependency when running it.

## Reference(s):

- [Server-resolved source repository](https://github.com/zengfr/AutoCoding/tree/main/docs/generated-skills/ultravibe)
- [ClawHub skill release](https://clawhub.ai/zengfr/skills/ultravibe)

## Skill Output:

**Output Type(s):** [Guidance, Workflow routing]

**Output Format:** [Markdown instructions with an inline shell command example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes one user request to one workflow; defaults to feature when no intent is identified or intents conflict.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
