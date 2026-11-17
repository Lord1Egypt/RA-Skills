## Description:

SeedDrop monitors Bilibili, Tieba, Zhihu, and Xiaohongshu discussions, scores relevant posts, and drafts value-first replies for manual approval using encrypted credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[2019-02-18](https://clawhub.ai/user/2019-02-18)

### License/Terms of Use:

MIT-0

## Use Case:

External users, small businesses, and indie developers use SeedDrop to find relevant community discussions and prepare helpful, platform-appropriate replies that can be reviewed before posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses authenticated social-platform sessions, full cookies, and browser automation.

Mitigation: Use only intended accounts, keep credentials in SocialVault, restrict browser and cookie access to the target platforms, and avoid exposing session material in logs or prompts.

Risk: Generated replies could be inaccurate, promotional, or unsuitable for a platform context.

Mitigation: Keep manual approval enabled for every posting action and review each draft before it is sent.

Risk: Posts and comments from monitored platforms are untrusted third-party content.

Mitigation: Treat collected text as untrusted input and review generated actions for instruction-following, policy, and brand-safety issues before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/2019-02-18/skills/seed-drop)
- [Safety Rules](artifact/references/safety-rules.md)
- [Scoring Criteria](artifact/references/scoring-criteria.md)
- [Platform TOS Notes](artifact/references/platform-tos-notes.md)
- [Quickstart Guide](artifact/guides/quickstart.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSONL pipeline outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply drafts require human approval before posting.]

## Skill Version(s):

1.0.4 (source: server release metadata; package and skill metadata report 3.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
