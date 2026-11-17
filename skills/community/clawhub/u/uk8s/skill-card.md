## Description:

Creates a UK8S Kubernetes cluster through ucloud-cli by discovering VPC, subnet, Kubernetes version, and image settings, then generating and submitting the cluster creation request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hellohjc](https://clawhub.ai/user/hellohjc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to provision a UCloud UK8S cluster from an agent session after confirming UCloud CLI configuration and required project and network settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create paid UCloud infrastructure.

Mitigation: Require explicit user approval before submitting the cluster creation request and show the selected region, project, node counts, and charge type before provisioning.

Risk: The skill may install ucloud-cli from GitHub during setup.

Mitigation: Verify the download source and package integrity before execution, or require the user to install and configure ucloud-cli independently.

Risk: The skill handles a generated cluster password in temporary files and chat output.

Mitigation: Use private temporary files that are deleted after use and avoid exposing plaintext credentials in the transcript unless the user explicitly accepts that handling.

## Reference(s):

- [UK8S API](https://docs.ucloud.cn/api/uk8s-api/)
- [VPC API](https://docs.ucloud.cn/api/vpc-api/README)
- [ucloud-cli](https://github.com/ucloud/ucloud-cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes generated cluster details and operational follow-up commands when provisioning succeeds.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
