## Description:

Automates Xianyu listing workflows by helping an agent prepare product details, upload images, set prices, and publish or manage listings through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers and agents use this skill to automate Xianyu item listing workflows, including product information entry, image upload, price setting, batch posting, login status management, and listing maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates live Xianyu account actions, including publishing and unpublishing listings.

Mitigation: Run it only in an isolated, non-shared environment with an account prepared for automation, and manually confirm each listing action.

Risk: Saved login state can persist account access on the local machine.

Mitigation: Clear saved login sessions after use and avoid running the skill on shared systems.

Risk: Batch, scheduled, or frequent posting can create platform or account risk.

Mitigation: Avoid batch or scheduled posting unless the effects are fully understood, control posting frequency, and follow Xianyu platform rules.

Risk: The security summary says the scope, install path, and guardrails are not clear enough for a marketplace publishing tool.

Mitigation: Review the skill carefully before installation, pin dependencies where possible, align the runtime with the shipped code, and require explicit confirmation before publishing or unpublishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/onlyloveher/skills/xianyu-publisher)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)
- [Xianyu publish page](https://2.taobao.com/publish/xianyu)
- [Taobao login page](https://login.taobao.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and structured product data examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser automation steps and product listing configuration; users should confirm live account actions before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
