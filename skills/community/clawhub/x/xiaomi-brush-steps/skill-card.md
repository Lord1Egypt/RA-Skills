## Description:

华米运动(Zepp/小米运动)自动刷步数技能，支持多账号管理。当用户提到刷步数、修改运动步数、华米运动、小米运动、手环步数时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckxgzxa](https://clawhub.ai/user/ckxgzxa)

### License/Terms of Use:

MIT-0

## Use Case:

External users who choose to automate Zepp Life or Xiaomi sports step-count updates use this skill to configure one or more accounts, run the bundled Python workflow, and receive a per-account success or failure report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Zepp or Xiaomi account passwords may be stored locally in config.json in plaintext.

Mitigation: Avoid storing real account passwords unless the user accepts the local exposure risk; prefer a version that prompts per run or uses a secure secret store.

Risk: The skill text points users to third-party testing websites that could receive account credentials.

Mitigation: Do not enter Zepp or Xiaomi passwords into the listed third-party testing websites.

Risk: Scheduled runs can continue changing account step counts after initial setup.

Mitigation: Do not enable scheduled runs unless the exact cron job has been reviewed and the user knows how to remove it.

Risk: Fake source-IP headers can obscure request provenance and add operational risk.

Mitigation: Prefer a version that removes fake source-IP headers; keep fake-IP behavior disabled where configurable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckxgzxa/skills/xiaomi-brush-steps)
- [Zepp registration token endpoint](https://api-user.zepp.com/v2/registrations/tokens)
- [Huami client login endpoint](https://account.huami.com/v2/client/login)
- [Huami band data endpoint](https://api-mifit-cn.huami.com/v1/data/band_data.json)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Console text report with Markdown-style command and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, requests, and pycryptodome; reads account and step-range settings from local config.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
