## Description:

One-command disk cleanup for macOS and Linux covering trash, caches, temp files, old kernels, snap revisions, Homebrew, Docker, and Xcode artifacts, with dry-run support and no dependencies beyond bash and awk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[camopel](https://clawhub.ai/user/camopel)

### License/Terms of Use:


## Use Case:

Developers, engineers, and operators use this skill to preview and run cross-platform disk cleanup when storage is low or accumulated caches and build artifacts need to be reclaimed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleanup script can delete user and system resources immediately, including some operations that may use sudo.

Mitigation: Run `bash scripts/cleanup.sh --dry-run` first and review the proposed cleanup before allowing changes.

Risk: High-impact categories such as kernels, Docker resources, snaps, and Homebrew packages may remove resources the user still needs.

Mitigation: Use skip flags such as `--skip-kernels`, `--skip-docker`, `--skip-snap`, and `--skip-brew` unless those categories are intentionally in scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/camopel/skills/storage-cleanup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash commands and cleanup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run execution before cleanup and skip flags for higher-impact categories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
