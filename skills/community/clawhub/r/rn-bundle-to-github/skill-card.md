## Description:

Guides agents through bundling a React Native app for Android and iOS and publishing release or debug bundles to GitHub Releases with versioning and changelog steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvtong199881](https://clawhub.ai/user/lvtong199881)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to prepare React Native JavaScript bundles, publish production or debug GitHub Releases, and document version changes for hot-update workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow relies on a remotely fetched publish.sh script that can run with repository credentials and publishing authority.

Mitigation: Inspect or vendor the script before use, prefer a pinned commit plus checksum, and avoid piping or executing unreviewed remote content.

Risk: Executing the release workflow can change package.json, CHANGELOG.md, commits, tags, remote branches, and GitHub Releases.

Mitigation: Use a clean working tree, a review branch, repository backups or rollback tags, and a fine-grained GitHub token limited to the target repository.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lvtong199881/skills/rn-bundle-to-github)
- [Remote publish.sh referenced by the skill](https://raw.githubusercontent.com/lvtong199881/MyRNApp/refs/heads/main/publish.sh)
- [GitHub Releases API endpoint pattern](https://api.github.com/repos/{owner}/{repo}/releases)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with bash commands, API endpoint examples, file layout examples, and a Kotlin integration snippet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide changes to package.json, CHANGELOG.md, git tags, remote branches, and GitHub Releases when the referenced workflow is executed.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
