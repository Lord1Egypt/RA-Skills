## Description: <br>
Coordinates an event-driven workflow that validates confirmed meeting issue drafts, creates linked Gitea issues for single-project meetings, updates meeting metadata, and returns email notification payloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[myd2002](https://clawhub.ai/user/myd2002) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project teams use this skill with OpenClaw and Gitea to convert confirmed meeting action items into repository issues, meeting status updates, and notification-ready email payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify Gitea repositories and meeting status records. <br>
Mitigation: Restrict the bot token to intended repositories and add status and approval checks inside create_issues.py and finish.py before deployment. <br>
Risk: The webhook may be exposed with weak defaults. <br>
Mitigation: Run it only in a trusted Gitea environment, require HTTPS, and set WEBHOOK_SECRET. <br>
Risk: Meeting content, contact data, and generated email payloads may contain sensitive information. <br>
Mitigation: Treat email outputs and logs as sensitive and limit access to the configuration, webhook logs, and target repositories. <br>
Risk: Shell sourcing of the .env file can execute unintended content. <br>
Mitigation: Replace shell sourcing with safe key/value parsing before operational use. <br>
Risk: The package may not run correctly as published because security evidence reports Python syntax errors in check.py and finish.py. <br>
Mitigation: Fix and test those scripts before enabling the workflow. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/myd2002/skill-d-create-issues) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, API Calls, Configuration] <br>
**Output Format:** [JSON command responses with Markdown issue bodies and HTML email payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates Gitea issues, meeting metadata, and log entries when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
