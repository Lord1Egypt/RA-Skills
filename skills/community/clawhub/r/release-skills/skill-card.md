## Description:

Release Skills helps agents prepare software releases by detecting project version files, analyzing conventional commits, generating multi-language changelogs, proposing semantic version bumps, and guiding commit, tag, and optional push steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and release maintainers use this skill to prepare versioned releases across Node.js, Python, Rust, Claude Plugin, and generic projects. It supports changelog generation, semantic version selection, release summaries, git tagging, and optional push workflows after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary flags broad install or activation and a high-impact git release workflow as requiring review before installation.

Mitigation: Review the skill before installing, especially for global skill directories, and prefer a pinned trusted commit or release.

Risk: Release actions can change repository files, create commits and tags, or push changes to a remote branch.

Mitigation: Run dry-run or preview first, then confirm the exact repository, branch, files, version, commit, tag, and push target before allowing changes.

Risk: Generated changelog entries or semantic version bumps may not reflect project intent if commit messages are incomplete or ambiguous.

Mitigation: Review the proposed changelog and version bump before committing or tagging the release.

## Reference(s):

- [Release Skills on ClawHub](https://clawhub.ai/wpank/skills/release-skills)
- [README installation link](https://github.com/wpank/ai/tree/main/skills/tools/release-skills)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with shell command snippets, changelog entries, release summaries, and proposed file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform version-file, changelog, commit, tag, and push actions; dry-run and explicit confirmation are expected for high-impact release steps.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
