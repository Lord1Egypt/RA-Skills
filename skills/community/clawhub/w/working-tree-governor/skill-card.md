## Description:

Govern dirty git working trees by classifying runtime noise vs real source changes, defaulting to selective staging, verifying staged scope, and asking the operator when scope is ambiguous.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lobsterquant](https://clawhub.ai/user/lobsterquant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect dirty git working trees, separate source and test changes from runtime noise, stage only relevant files, and ask for operator approval when commit scope is ambiguous.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill influences git staging and commits, so overly broad or incorrect application could stage unrelated source changes or runtime-sensitive files.

Mitigation: Follow its selective staging and staged-scope verification steps, and require operator approval when scope is ambiguous or larger than expected.

Risk: Dirty working trees may contain logs, runtime state, caches, generated outputs, or forensic snapshots that should remain out of history.

Mitigation: Classify changed paths into the documented buckets and preserve or exclude runtime noise, logs, caches, generated outputs, and forensics by default.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lobsterquant/skills/working-tree-governor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dirty-tree summaries, bucket classifications, selective staging recommendations, verification checks, and operator questions when scope is ambiguous.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
