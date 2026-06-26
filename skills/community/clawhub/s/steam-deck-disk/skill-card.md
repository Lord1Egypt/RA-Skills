## Description: <br>
Helps manage and optimize Steam Deck disk space by checking disk usage, cleaning caches and logs, moving large files to /home, and guiding /var storage adjustments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jy00801119](https://clawhub.ai/user/jy00801119) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Steam Deck users and support agents use this skill to inspect partition usage, identify safe cleanup options, remove caches and logs after approval, and plan storage changes for constrained system partitions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic cleanup can delete caches, temporary files, logs, or backups without enough user review. <br>
Mitigation: Keep automatic cleanup disabled by default, show each deletion target before execution, and require explicit user approval for destructive commands. <br>
Risk: /var expansion and bind-mount guidance can make persistent root-level storage changes on the Steam Deck. <br>
Mitigation: Require current backups, verify the exact SteamOS partition layout, and reserve partition or mount changes for users who understand the recovery path. <br>
Risk: Disk reports or cleanup recommendations may be stale after files change. <br>
Mitigation: Run disk checks before and after cleanup, report the observed state, and avoid acting on older recorded partition usage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jy00801119/steam-deck-disk) <br>
- [Steam Deck /var expansion guide](var-expansion-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and cleanup checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only; output should report disk state, proposed cleanup actions, expected impact, and post-cleanup verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
