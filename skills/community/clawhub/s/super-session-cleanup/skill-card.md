## Description: <br>
Session cleanup skill for Claw-family agents that tracks and cleans up temporary files, scripts, installed skills, libraries, and software generated during a conversation session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaobs](https://clawhub.ai/user/chaobs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to start session artifact tracking, review generated files, packages, skills, and software, and clean up transient resources with confirmation for higher-risk removals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup script can uninstall packages or delete skill directories based on tracked data. <br>
Mitigation: Use dry-run first, inspect session-track.json, and require explicit confirmation before package uninstalls, skill removal, or non-temporary path deletion. <br>
Risk: Tracked paths or packages may include entries the user still needs. <br>
Mitigation: Review the categorized checklist and use the skip list for items that should be preserved before executing cleanup. <br>


## Reference(s): <br>
- [Session Cleanup Reference Guide](references/cleanup-guide.md) <br>
- [ClawHub release page](https://clawhub.ai/chaobs/super-session-cleanup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tracking data and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .workbuddy/session-track.json and may propose deletion or uninstall commands during cleanup.] <br>

## Skill Version(s): <br>
1.4.0 (source: frontmatter, server release metadata, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
