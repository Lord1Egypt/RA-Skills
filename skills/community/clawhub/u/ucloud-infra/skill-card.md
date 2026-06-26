## Description: <br>
UCloud Cloud Management - Complete Version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage UCloud infrastructure resources from an agent workflow, including hosts, databases, caches, networking, storage, load balancers, firewall rules, projects, and regions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles powerful UCloud credentials and can perform destructive cloud operations. <br>
Mitigation: Use least-privilege UCloud keys for a test or limited project, avoid production credentials until command execution and secret handling are reviewed, and require manual approval for destructive operations. <br>
Risk: Create and delete operations write structured logs that may expose operational details. <br>
Mitigation: Protect the generated logs directory, review retention and access controls, or disable logging where sensitive operational metadata should not be stored locally. <br>


## Reference(s): <br>
- [UCloud CLI installation guide](https://github.com/UCloudDoc-Team/cli/blob/master/intro.md) <br>
- [UCloud console](https://console.ucloud.cn/) <br>
- [ClawHub skill page](https://clawhub.ai/qianjunye/ucloud-infra) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, JSON, guidance] <br>
**Output Format:** [JSON responses and Markdown usage guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Create and delete operations are logged to JSONL files in a local logs directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
