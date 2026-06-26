## Description: <br>
Ssh Deploy Skill helps agents manage Linux servers over SSH with batch command execution, file transfer, and templated software installation using domestic mirror optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awamwang](https://clawhub.ai/user/awamwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, DevOps engineers, and agents use this skill to configure SSH inventories, execute commands across one or more Linux servers, transfer files, and run reusable installation templates for common server software. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad remote changes across multiple Linux servers. <br>
Mitigation: Use a dedicated least-privilege deployment account, test commands and templates on one non-production host first, and limit batch targets to the intended inventory group or tag. <br>
Risk: The skill can read SSH configuration details and use them for remote access. <br>
Mitigation: Review ~/.ssh/config exposure before installation and only run the skill in environments where agent access to those SSH entries is intended. <br>
Risk: Weak host key handling can expose production deployments to host impersonation risk. <br>
Mitigation: Enable strict host key checking for production and verify new host fingerprints before first use. <br>
Risk: Stored passwords or privileged credentials in inventory files can be exposed to the agent runtime. <br>
Mitigation: Avoid passwords in inventory.json, prefer SSH keys, and use environment variables or an external secrets process for sensitive installation parameters. <br>
Risk: Package-source and service-changing templates may alter system repositories, package managers, or running services. <br>
Mitigation: Review each template before use and validate package mirror or service changes on a non-production host before applying them broadly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/awamwang/ssh-deploy-skill) <br>
- [Best Practices](references/best-practices.md) <br>
- [Domestic Mirror Configuration](references/mirrors.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Aliyun PyPI mirror](https://mirrors.aliyun.com/pypi/simple) <br>
- [npmmirror registry](https://registry.npmmirror.com) <br>
- [USTC Docker mirror](https://docker.mirrors.ustc.edu.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands, Python commands, JSON configuration examples, and shell script templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may guide remote command execution, file transfer, inventory edits, and package or service changes on target Linux servers.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
