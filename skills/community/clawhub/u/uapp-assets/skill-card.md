## Description: <br>
查询友盟账户下的 App 和小程序资产，帮助代理通过 umeng-cli 调用只读 OpenAPI 获取应用数量、应用列表和小程序列表。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squall0925](https://clawhub.ai/user/squall0925) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to discover Umeng account-level App and mini-program assets before summarizing inventories or passing AppKeys to downstream Umeng skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on cached Umeng credentials for account-wide asset queries. <br>
Mitigation: Install and use it only in environments where the Umeng CLI and cached credentials are trusted and access is appropriate for the account being queried. <br>
Risk: The artifact instructs agents to send usage telemetry and may include AppKeys in trace events. <br>
Mitigation: Require user or operator consent before running trace commands, and avoid sending AppKeys as telemetry unless explicitly approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/squall0925/uapp-assets) <br>
- [Umeng CLI homepage](https://github.com/umeng/umeng-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces read-only Umeng asset lookup guidance and may surface AppKeys or dataSourceIds for downstream skills.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
