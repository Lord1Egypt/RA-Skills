## Description:

Fix failing tests without weakening them — run the suite once, rerun only the failing files to separate flaky from real failures, classify each real failure as source bug or wrong test, then propose minimal diffs for approval. Use when asked to fix failing tests or make the suite green.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winsoftlabs30](https://clawhub.ai/user/winsoftlabs30)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to triage a failing test suite, distinguish flaky failures from consistent failures, decide whether each consistent failure points to a source bug or an incorrect test, and prepare minimal proposed patches for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The npx test commands may download an unpinned package when the test tool is not installed locally.

Mitigation: Check that the package source is trusted before running the command; prefer a locally installed or explicitly pinned test runner.

## Reference(s):

- [Test Fix on ClawHub](https://clawhub.ai/winsoftlabs30/skills/test-fix)
- [Test Fix on skills.sh](https://skills.sh/WinSoftLabs30/test-fix-skill)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code]

**Output Format:** [Markdown with shell commands and unified diff code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Failure summaries, flaky or consistent classifications, and proposed minimal diffs; patches are held for approval.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
