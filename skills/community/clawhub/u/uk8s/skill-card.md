## Description: <br>
Creates UK8S Kubernetes clusters by using ucloud-cli to discover VPC, subnet, Kubernetes version, and image settings, then generate and submit a create-cluster request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hellohjc](https://clawhub.ai/user/hellohjc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to create a UCloud UK8S Kubernetes cluster with predefined master, node, storage, and network settings after confirming account configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create billable UCloud infrastructure. <br>
Mitigation: Confirm the target project, region, zone, resource sizes, and expected charges before running the create-cluster API call. <br>
Risk: The skill may install ucloud-cli from a downloaded release package. <br>
Mitigation: Verify the ucloud-cli download source and integrity before installation, or install the CLI through an approved internal process. <br>
Risk: The skill can print a generated admin password in the conversation or logs. <br>
Mitigation: Avoid shared or logged chats for password output and rotate the generated password immediately after cluster creation. <br>


## Reference(s): <br>
- [UK8S API](https://docs.ucloud.cn/api/uk8s-api/) <br>
- [VPC API](https://docs.ucloud.cn/api/vpc-api/README) <br>
- [ucloud-cli](https://github.com/ucloud/ucloud-cli) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, API calls, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create /tmp/create_uk8s.json during execution and may report cluster details, status guidance, and a generated admin password.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
