## Description:

Deploys WeChat Mini Programs to WeChat CloudBase by guiding cloud function deployment, manual collection setup, frontend upload through miniprogram-ci, and common real-environment failure diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincent-chao-lang](https://clawhub.ai/user/vincent-chao-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to deploy WeChat Mini Programs backed by CloudBase, upload trial or development builds, and troubleshoot CloudBase CLI, database collection, upload whitelist, and region issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run authenticated CloudBase deployment and Mini Program upload actions.

Mitigation: Require explicit user-provided identifiers and local key file paths, review target environment details before execution, and keep review and release as manual human actions.

Risk: Upload may require weakening the Mini Program upload IP whitelist when the network egress is IPv6.

Mitigation: Prefer an approved IPv4 egress and whitelist entry; if the whitelist is disabled temporarily, document the exception and re-enable it immediately after upload.

Risk: The documented workflow installs mutable deployment tooling.

Mitigation: Use a pinned CloudBase CLI version for repeatable deployments and verify the installed tooling before running authenticated commands.

## Reference(s):

- [WeChat CloudBase deployment pitfalls](references/pitfalls.md)
- [ClawHub skill page](https://clawhub.ai/vincent-chao-lang/skills/wechat-miniprogram-cloudbase-deploy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and parameterized script usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided AppID, CloudBase environment ID, subscribe template ID, and a local upload key file path; key contents should not be pasted into chat.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
