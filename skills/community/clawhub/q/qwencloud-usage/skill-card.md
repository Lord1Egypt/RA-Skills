## Description: <br>
[QwenCloud] Manage account auth and query usage/billing. Use for: login, logout, check usage, view billing, free tier quota, coding plan status, pay-as-you-go costs. Skip for: model browsing, non-account tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to authenticate with the QwenCloud CLI and answer account-level questions about usage, free-tier quota, coding plan status, and pay-as-you-go billing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires installing and invoking the external QwenCloud CLI, including a global npm install step. <br>
Mitigation: Install only if the QwenCloud CLI is trusted, and review the global npm install command before use. <br>
Risk: The skill can let an agent access QwenCloud account status, quotas, usage, billing details, and credential storage behavior. <br>
Mitigation: Review credential-storage settings and allow access only when the agent is permitted to handle QwenCloud account and billing information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, JSON, Markdown] <br>
**Output Format:** [Markdown guidance with shell command examples and structured JSON CLI output handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prefers explicit --format json for agent use, with human-readable summaries produced from parsed CLI responses.] <br>

## Skill Version(s): <br>
0.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
