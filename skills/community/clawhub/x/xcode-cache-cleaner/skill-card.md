## Description:

Xcode Cache Cleaner helps iOS/macOS developers dry-run and clean global Xcode caches and per-project build artifacts to reclaim disk space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symbolstar](https://clawhub.ai/user/symbolstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect Xcode and project build caches, run a dry-run report, and execute cleanup only after reviewing the affected paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted project directory name can cause unintended shell command execution in the project cleanup script.

Mitigation: Review before installing, use dry-run first, and do not run artifact/scripts/clean-cache.sh on untrusted or externally supplied directory names until the eval-based find construction is fixed.

Risk: Cleanup can delete signed archive builds when archive deletion is explicitly enabled.

Mitigation: Inspect dry-run output and avoid --include-archives unless the archive scope is already approved or backed up.

Risk: Using --yes skips the confirmation prompt for file deletion.

Mitigation: Avoid --yes unless the cleanup scope has already been reviewed and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/symbolstar/skills/xcode-cache-cleaner)
- [Publisher Profile](https://clawhub.ai/user/symbolstar)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with shell command examples and cleanup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes dry-run review before destructive cleanup.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
