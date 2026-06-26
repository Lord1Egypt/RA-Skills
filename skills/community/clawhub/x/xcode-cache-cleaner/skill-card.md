## Description: <br>
Scans project directories and global Xcode cache locations, reports reclaimable space, and guides optional cleanup of build artifacts such as DerivedData, DeviceSupport folders, simulator leftovers, package caches, and test bundles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[symbolstar](https://clawhub.ai/user/symbolstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need to understand and reduce disk usage from Xcode, Swift/iOS project, and related build caches on a Mac development machine. It is intended to produce a dry-run report first, then guide confirmed cleanup actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup scripts can delete local build caches and, with `--include-archives`, signed Xcode archives. <br>
Mitigation: Run `--dry-run` first, verify every listed path, keep archives unless they are backed up, and get explicit confirmation before deletion. <br>
Risk: `--yes` skips the interactive confirmation prompt. <br>
Mitigation: Use `--yes` only after the exact dry-run output has been reviewed and approved. <br>
Risk: Project cleanup has an unsafe edge case for untrusted or oddly named directories because of command construction in the scanner loop. <br>
Mitigation: Avoid running project cleanup on untrusted paths until the command construction is fixed; prefer trusted project directories with reviewed dry-run output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/symbolstar/xcode-cache-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and cleanup summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for dry-run review and confirmation before destructive cleanup; may include concrete keep patterns or cleanup flags.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
