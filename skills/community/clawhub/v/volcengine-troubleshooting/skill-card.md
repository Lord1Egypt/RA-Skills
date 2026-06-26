## Description: <br>
Use when the user encounters VolcEngine errors or needs local troubleshooting for OpenAPI, Python SDK, CLI, IAM, billing, compute, networking, storage, database, CDN, media, AI, security, or VKE cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to triage VolcEngine failures, collect minimal local context, route issues to the right product domain, and propose read-only diagnostic checks before any confirmed change. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may operate in environments with VolcEngine credentials and sensitive account context. <br>
Mitigation: Use least-privilege temporary credentials where possible, avoid secret-value or token-minting permissions unless explicitly needed, and mask AccessKeyId values while never printing SecretKey or SessionToken values. <br>
Risk: Some troubleshooting paths can lead to commands that reveal API keys, role credentials, workload tokens, SecretValue, user data, or full console output. <br>
Mitigation: Require manual approval before any command that could reveal sensitive values, and prefer read-only Describe/List/Get/Query/Lookup/Check operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/volc-sdk-team/volcengine-troubleshooting) <br>
- [Getting Started](references/getting-started.md) <br>
- [OpenAPI Quick Check](references/openapi-quick-check.md) <br>
- [Domain Troubleshooting Guides](references/domain-guides/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, code, configuration] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic posture by default; credentials and sensitive account details should be masked or omitted.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
