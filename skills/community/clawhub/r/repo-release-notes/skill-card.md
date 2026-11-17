## Description:

Drafts release notes and changelog entries from local Git history for commit summaries, ref comparisons, version notes, and user-facing changelogs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aboxhq](https://clawhub.ai/user/aboxhq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to inspect local Git history, compare refs or tags, and draft concise release notes or changelog entries grouped by user impact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local Git history may contain sensitive commit messages, file names, or unreleased product details.

Mitigation: Use the skill only in repositories whose history is acceptable for the agent to read.

Risk: Generated release notes may overstate impact or omit important breaking, migration, or security details.

Mitigation: Review generated release notes before publishing and confirm claims against commits, diffs, and release requirements.

Risk: Untrusted refs, branch names, or paths could lead to unsafe command construction if handled carelessly.

Mitigation: Treat user-provided refs and paths as data and prefer read-only Git commands.

## Reference(s):

- [Repo Release Notes on ClawHub](https://clawhub.ai/aboxhq/skills/repo-release-notes)
- [Release Note Style](artifact/references/release-note-style.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown release-note draft with optional inline Git command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries include release range and date when known, categorized changes, upgrade notes when applicable, and assumptions about tags or uncommitted changes.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
