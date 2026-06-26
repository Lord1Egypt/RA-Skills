## Description: <br>
Monitor download counts for your ClawHub-published skills. Track changes over time with automated alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsag1](https://clawhub.ai/user/tsag1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to monitor ClawHub download counts, record local history, generate daily, weekly, and monthly summaries, and send configured Feishu notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Feishu credentials stored in environment variables or the local .env file are sensitive. <br>
Mitigation: Restrict access to the tracker data directory and avoid sharing the .env file. <br>
Risk: Monitored skill slugs, notes, local reports, and Feishu messages can reveal private project names or usage patterns. <br>
Mitigation: Monitor only slugs and notes that are appropriate to store locally and send to Feishu. <br>
Risk: The skill executes local Python and shell scripts and calls the ClawHub CLI for each monitored slug. <br>
Mitigation: Install only when download tracking is intended and review the configured skills.csv before scheduled execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tsag1/skill-download-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/tsag1) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text reports with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local CSV history and report archives, prints summaries to stdout, and sends Feishu notifications when credentials are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
