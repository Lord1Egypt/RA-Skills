## Description:

Controls Xiaomi Mi Home smart devices, including lights, air conditioners, robot vacuums, scenes, and device status checks, through assistant commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanlan314](https://clawhub.ai/user/lanlan314)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to sign in to a Xiaomi account and control supported Xiaomi Mi Home devices through natural-language smart-home commands. It can list devices, check status, trigger scenes, and issue device-control actions when the required Xiaomi and Feishu credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests full Xiaomi login credentials and can pass login or CAPTCHA flow data through the assistant or Feishu.

Mitigation: Install only after security review, use dedicated least-privilege accounts where possible, and avoid entering credentials unless the deployment path is trusted.

Risk: The skill caches Xiaomi bearer-token material locally.

Mitigation: Store token files with restrictive permissions, rotate credentials after testing, and clear cached tokens when uninstalling or moving the environment.

Risk: The security verdict is suspicious because token handling, hardcoded defaults, and login flow design require careful review.

Mitigation: Prefer a release that uses official delegated login, removes hardcoded secrets, and scopes access to only the device-control operations needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lanlan314/skills/xiaomi-miot-lan)
- [ClawHub publisher profile](https://clawhub.ai/user/lanlan314)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, Python code, shell commands, and JSON-like device or card payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request Xiaomi credentials, CAPTCHA input, Feishu app credentials, and local environment-variable configuration.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
