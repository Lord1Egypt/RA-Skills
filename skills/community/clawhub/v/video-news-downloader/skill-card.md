## Description: <br>
Automates daily downloads of CBS Evening News and BBC News at Ten from YouTube, extracts English subtitles, prepares DeepSeek proofreading prompts, and serves the videos through local HTTP players. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cyberpsychosissss](https://clawhub.ai/user/Cyberpsychosissss) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to automate scheduled news video downloads, subtitle extraction, proofreading preparation, local HTTP playback, and cron-based update management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent daily cron jobs for downloading videos and preparing subtitle proofreading tasks. <br>
Mitigation: Install cron jobs only after confirming the recurring schedule is desired, review existing crontab entries, and use the provided status or remove commands to audit or remove the jobs. <br>
Risk: The skill can run HTTP video servers on ports 8093 and 8095 that may be reachable from untrusted networks. <br>
Mitigation: Confirm those ports are not exposed outside trusted networks before starting the servers, and use firewall or network controls when local-only streaming is intended. <br>
Risk: Subtitle text may be shared with DeepSeek if a user manually submits the generated proofreading prompt. <br>
Mitigation: Review generated proofreading task files before submission and share subtitle text only when it is acceptable to send that content to DeepSeek. <br>


## Reference(s): <br>
- [Detailed workflow](references/workflow.md) <br>
- [Cron job setup guide](references/cron-setup.md) <br>
- [ClawHub listing](https://clawhub.ai/Cyberpsychosissss/video-news-downloader) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and Python and shell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local video, subtitle, proofreading task, correction report, log, cron, and HTTP server artifacts when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
