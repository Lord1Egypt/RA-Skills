## Description: <br>
Guides a user through reclaiming macOS disk space by deleting user cache files with a Terminal command. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olegmayami45-boop](https://clawhub.ai/user/olegmayami45-boop) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Mac users and support agents use this skill to free disk space by walking through a Terminal-based cleanup of the current user's cache directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup command permanently deletes files from the current user's cache directory. <br>
Mitigation: Before running it, confirm the command is exactly `rm -rf ~/Library/Caches/*` and that only cache files are being targeted. <br>
Risk: The skill presents the cleanup as safe even though deletion is irreversible. <br>
Mitigation: Use it only when the user understands that deleted cache files are not recoverable and apps may need to regenerate cache data. <br>
Risk: A password or permission prompt could expand the impact if the user does not understand why macOS is asking. <br>
Mitigation: Avoid entering a password unless macOS clearly explains why permission is needed for the intended cache cleanup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olegmayami45-boop/reclaim-disk-space-on-your-mac) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes user-directed Terminal cleanup instructions for macOS cache files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
