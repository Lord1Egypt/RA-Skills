## Description: <br>
Qinglong helps agents administer Qinglong Panel tasks, environment variables, scripts, subscriptions, dependencies, and system settings through HTTP API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awsl1110](https://clawhub.ai/user/awsl1110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators who manage Qinglong Panel instances can use this skill to translate natural language requests into authenticated API calls for cron jobs, environment variables, scripts, subscriptions, dependencies, and system settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad administrative and host-level control over a Qinglong panel. <br>
Mitigation: Install only when that control is intended, use a non-production or least-privilege account where possible, and require explicit confirmation before delete, import/export, system update/reload, dependency change, or shell command actions. <br>
Risk: Reusable passwords or tokens could be exposed while configuring authenticated API access. <br>
Mitigation: Prefer HTTPS, avoid sharing reusable passwords in chat, and rotate credentials after testing. <br>


## Reference(s): <br>
- [Qinglong API reference](https://qinglong.online/api/) <br>
- [Bundled API reference](artifact/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with curl commands, tables or lists, and summarized API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated HTTP requests that change Qinglong panel state.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
