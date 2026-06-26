## Description: <br>
Release Skills provides a universal release workflow with project auto-detection, semantic versioning, multi-language changelog generation, and Git tagging guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and release maintainers use this skill to prepare software releases by detecting version files, analyzing commits, recommending version bumps, generating changelogs, and guiding confirmed Git release steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Release automation may change version or changelog files and guide Git commit, tag, or push steps in the wrong branch, remote, or account. <br>
Mitigation: Use dry-run first, review proposed file edits and release commands, and approve commit, tag, or push actions only after confirming the branch, remote, and account. <br>
Risk: Commit analysis may recommend an incorrect semantic version bump or produce changelog entries that need editorial review. <br>
Mitigation: Review the proposed version bump and generated changelog content before applying changes; use explicit major, minor, or patch options when the recommendation is wrong. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wpank/release-skills) <br>
- [Release Skills repository path referenced by README](https://github.com/wpank/ai/tree/main/skills/tools/release-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with release summaries, changelog entries, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run previews, version bump recommendations, changelog updates, and Git commit, tag, or push command sequences.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
