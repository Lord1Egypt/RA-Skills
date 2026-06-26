## Description: <br>
File-based X/Twitter post scheduler that lets users drop tweets into day/time folders for automatic posting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[madebydia](https://clawhub.ai/user/madebydia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to set up and run a local filesystem-backed queue for scheduled X/Twitter posts, threads, community posts, and media attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queued text, community IDs, images, and videos may be uploaded publicly or to the selected X community. <br>
Mitigation: Review queue contents and community targets before enabling cron posting; use dry-run mode or validation before live posting. <br>
Risk: The posting script requires X OAuth credentials and can optionally query macOS Keychain when configured. <br>
Mitigation: Prefer environment variables for credentials, avoid committing secrets, and leave keychain fallback unset unless that behavior is intended. <br>
Risk: If deleteAfterPost is disabled, scheduled files can post again on the next weekly cycle. <br>
Mitigation: Keep deleteAfterPost enabled for one-time posts or manually remove posted files after each run. <br>


## Reference(s): <br>
- [Xqueue ClawHub listing](https://clawhub.ai/madebydia/xqueue) <br>
- [Xqueue GitHub repository](https://github.com/madebydia/xqueue) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with shell commands, configuration examples, and Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create queue folders, config.json, sample tweet files, and posted.log when the bundled setup and posting scripts are run.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
