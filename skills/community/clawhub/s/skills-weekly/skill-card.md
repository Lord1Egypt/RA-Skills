## Description: <br>
OpenClaw Skills Weekly tracks trending ClawHub skills and generates GitHubAwesome-style YouTube video scripts with two-track ranking for Movers and Rockets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ademczuk](https://clawhub.ai/user/ademczuk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content operators use this skill to collect ClawHub skill metrics, rank weekly movers and new releases, and generate Markdown reports plus voice-ready video scripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default workflow can make broad external API calls and use API keys for script generation and optional X/Twitter capture. <br>
Mitigation: Review before installing, run only where external calls are acceptable, prefer --skip-x unless X/Twitter capture is required, and provide least-privilege API keys. <br>
Risk: The workflow can copy or replace a local metrics database from a Docker container. <br>
Mitigation: Use --no-bridge unless Docker-to-host database copying is explicitly intended, and keep backups of local metrics data. <br>
Risk: The skill may install Python packages and write local reports, JSON output, and SQLite snapshot data. <br>
Mitigation: Run in a controlled workspace where package installation and local report or database writes are expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ademczuk/skills-weekly) <br>
- [ClawHub public skills API](https://clawhub.ai/api/v1/skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown reports, voice-ready plain text scripts, structured JSON, and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also write local SQLite snapshot data for ranking history.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
