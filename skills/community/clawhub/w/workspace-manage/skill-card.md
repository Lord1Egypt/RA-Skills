## Description: <br>
workspace-manager helps agents maintain an OpenClaw workspace with standard folders, file organization, cleanup, archiving, health audits, and optional Google Drive sync. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mslchy](https://clawhub.ai/user/mslchy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to audit workspace health, standardize expected directories, classify generated artifacts, clean temporary files, archive older artifacts, and optionally back up selected workspace content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The full pipeline can run the optional sync step and upload Workspace_Human content plus core configuration backups when gog is installed and authenticated. <br>
Mitigation: Run only the needed steps, such as audit or organize, and disable sync in config/sync-config.json or avoid authenticating gog unless cloud backup is intended. <br>
Risk: --dry-run does not fully preview every pipeline action because archiving is skipped in dry-run and sync behavior depends on gog configuration. <br>
Mitigation: Use individual script dry-runs or step-specific commands before broad maintenance, and review sync configuration before running pipeline.sh --all. <br>
Risk: Cleanup can move matched files to trash when execution is confirmed. <br>
Mitigation: Run cleanup.py without --execute first, review the proposed file list, and keep protected path settings aligned with workspace requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mslchy/workspace-manage) <br>
- [Publisher profile](https://clawhub.ai/user/mslchy) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate local logs and JSON cleanup reports when the bundled scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and changelog, released 2026-03-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
