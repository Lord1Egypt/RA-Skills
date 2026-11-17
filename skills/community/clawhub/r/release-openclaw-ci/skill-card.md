## Description:

Run, watch, debug, and summarize OpenClaw full release CI, release checks, live provider gates, install/update proofs, and release-secret preflights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to validate a frozen OpenClaw release candidate, monitor and recover CI runs, check provider and install/update gates, and assemble release evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked the skill suspicious because its release validation description is paired with a request to publish packages. The evidence does not confirm that publication completed, and some referenced paths were unresolved.

Mitigation: Review the skill’s publication behavior and confirm that requesting package and plugin publication fits your needs before installing; treat the scanner verdict as a caution because the evidence is incomplete.

## Reference(s):

- [Release CI Notes](artifact/references/release-ci-notes.md)
- [Full Release Validation](/reference/full-release-validation#post-merge-continuation-proof)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Text, Markdown]

**Output Format:** [Markdown with inline shell commands and release evidence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Release scope and publication steps require explicit operator approval.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
