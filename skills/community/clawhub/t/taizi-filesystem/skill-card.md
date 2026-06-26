## Description: <br>
Advanced filesystem operations - listing, searching, batch processing, and directory analysis for Clawdbot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to inspect, search, copy, and analyze local filesystem content with filters, structured output, dry-run support, and safety-oriented defaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate across broad local filesystem paths, which can expose or affect more files than intended. <br>
Mitigation: Start with narrow target paths, avoid broad home or system paths unless needed, and confirm path filters before running operations. <br>
Risk: Batch copy or overwrite actions can replace files if used without review. <br>
Mitigation: Run copy commands with --dry-run first, confirm destinations, and use --overwrite only when backups exist or replacement is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-filesystem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe filesystem paths, filters, search patterns, dry-run copy commands, directory trees, and analysis summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
