## Description: <br>
Securely store, manage, rotate, and integrate secrets such as API keys, passwords, and certificates in CI/CD pipelines using Vault, AWS Secrets Manager, and native platform tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandonwise](https://clawhub.ai/user/brandonwise) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and security engineers use this skill to plan secure storage, rotation, scanning, and delivery of secrets across CI/CD pipelines and Kubernetes deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples touch sensitive secret stores and CI/CD environments where unsafe copying could expose or misuse credentials. <br>
Mitigation: Replace placeholders, avoid development or root tokens, review commands that create or rotate secrets, and test changes outside production first. <br>
Risk: Secret-derived values could be exposed through logs or unpinned third-party build components. <br>
Mitigation: Mask secret values, avoid logging secret material, and pin third-party CI actions and container images before production use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash, YAML, HCL, and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guidance with examples that require environment-specific review before production use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
