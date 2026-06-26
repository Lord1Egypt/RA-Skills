## Description: <br>
Manage a self-hosted QingLong panel through REST API operations for cron jobs, environment variables, scripts, dependencies, subscriptions, logs, configuration, and system administration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nnnnzs](https://clawhub.ai/user/nnnnzs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent inspect and administer their own QingLong scheduled task panel, including cron jobs, environment variables, scripts, dependencies, subscriptions, logs, and selected system operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer powerful QingLong panel and host controls, including command execution, auth reset, update or reload, config save, script save or run, dependency install, and delete actions. <br>
Mitigation: Use a dedicated QingLong application with only the scopes needed for the intended task, list resources before modifying them, and require explicit human confirmation before high-impact or destructive actions. <br>
Risk: The skill requires sensitive QingLong credentials and caches access tokens for API calls. <br>
Mitigation: Protect OpenClaw configuration, shell profile secrets, and the token cache; rotate credentials if exposure is suspected; clear cached tokens when access should be revoked. <br>
Risk: Incorrect target configuration could cause the agent to operate on the wrong QingLong panel. <br>
Mitigation: Verify QINGLONG_URL and the returned panel details before making changes, especially before delete, script execution, dependency installation, system reload, command-run, or auth-reset actions. <br>


## Reference(s): <br>
- [QingLong Skill Setup Guide](references/setup.md) <br>
- [QingLong API Reference](references/api.md) <br>
- [QingLong Project](https://github.com/whyour/qinglong) <br>
- [ClawHub Skill Page](https://clawhub.ai/nnnnzs/qinglong-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the QingLong panel.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, QINGLONG_URL, QINGLONG_CLIENT_ID, and QINGLONG_CLIENT_SECRET.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
