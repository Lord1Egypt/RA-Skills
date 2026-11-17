## Description:

Generate a concise, reproducible release digest from a local git repository — grouped commits, subject/file stats, and a Markdown changelog — without any third-party API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to summarize changes between git refs, tags, or dates and draft reviewable release notes, changelog sections, pull request summaries, or weekly digests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated release notes may include sensitive or misleading commit messages, author names, or filenames from the target repository.

Mitigation: Review and redact the generated Markdown before sharing it outside the intended audience.

Risk: The skill reads git history from the repository path supplied by the user.

Mitigation: Run it only on repositories you intend to inspect and confirm the --repo, --since, and --until inputs before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/release-digest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown release digest with repository window, commit and contributor counts, grouped commits, and file-change statistics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic for the same git repository and --since/--until window; runs locally and does not publish releases or call third-party APIs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
