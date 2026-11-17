## Description:

自动登录凭据管理，在需要登录时自动填写账号密码，支持 GitHub、知乎、闲鱼、BotStreet 等平台。

This skill is ready for commercial/non-commercial use.

## Publisher:

[155143783](https://clawhub.ai/user/155143783)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to automate credential lookup and browser login form filling for supported services. Security evidence flags this release as high risk because it exposes plaintext passwords and API keys, so embedded credentials should be removed and rotated before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext account passwords and API keys are exposed in the skill text.

Mitigation: Remove embedded credentials, rotate every exposed secret, and use scoped secret references or a credential broker instead.

Risk: Automated login form filling can submit credentials to an unintended destination.

Mitigation: Require explicit approval for each login destination and validate the exact domain before autofill.

Risk: Shared secrets may be exposed through agent logs or outputs.

Mitigation: Never print raw passwords or API keys, redact logs, and limit secret access to the minimum required workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/155143783/skills/zaizai-auto-login)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes login workflow instructions; operational use should sanitize secrets and avoid exposing raw credentials in logs or outputs.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
