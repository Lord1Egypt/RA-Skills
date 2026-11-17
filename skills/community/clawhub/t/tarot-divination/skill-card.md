## Description:

塔罗牌占卜付费服务，每日为你抽取一张塔罗牌，解读牌意与运势指引。包含78张塔罗牌数据（大阿尔卡纳22张 + 小阿尔卡纳56张），每次占卜随机抽取一张牌，给你牌意解读和今日指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoshuai1](https://clawhub.ai/user/guoshuai1)

### License/Terms of Use:

MIT-0

## Use Case:

External users run this skill to create a paid tarot order and receive a daily one-card tarot reading with card meaning and practical guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid order flow ships unsafe payment defaults and payment verification should not be relied on for real paid fulfillment.

Mitigation: Replace and verify the payment recipient and cryptographic configuration before use, and redesign payment verification before relying on it commercially.

Risk: Order files and the local database can store user questions together with transaction metadata.

Mitigation: Review where order files and the database are written, disclose local storage behavior to users, and avoid entering sensitive questions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guoshuai1/skills/tarot-divination)
- [ClawHub Publisher Profile](https://clawhub.ai/user/guoshuai1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance, Files]

**Output Format:** [Plain text with shell command usage and local JSON/SQLite order records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces randomized tarot guidance after a paid-order flow; stores questions and order metadata locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
