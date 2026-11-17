## Description:

Scans and categorizes files in a selected directory, detects duplicates, and reorganizes them into a clear folder structure with dry-run, logging, and rollback safeguards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[underbench2-gif](https://clawhub.ai/user/underbench2-gif)

### License/Terms of Use:


## Use Case:

Developers and end users use this skill to inspect a chosen directory, preview an organization plan, and move files into a cleaner folder structure with traceable logs. It is suited for organizing downloads, project folders, duplicate files, and mixed document, media, code, archive, and data directories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may inspect file names, paths, and contents in the selected directory.

Mitigation: Run the skill only on directories you are comfortable letting the agent inspect.

Risk: Reorganization can move files into an unexpected structure if the proposed plan is wrong or the wrong directory is selected.

Mitigation: Use the dry run first, review proposed moves, and keep backups for important folders before allowing changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/underbench2-gif/skills/ub2-smart-file-organizer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown summary with proposed or executed file operations and a reorganization_log.txt change log]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry run is enabled by default; duplicates are moved to a _duplicates folder for manual review and files are not deleted.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
