## Description:

Automates social-content generation, review artifacts, and sequential posting or draft creation for X/Twitter, Weibo, Xiaohongshu, and WeChat through a logged-in local browser profile.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent workflows use this skill to prepare platform-specific social copy, generate structured review artifacts, and publish or save drafts across selected social platforms after account login and content review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post or reply from logged-in social-media accounts.

Mitigation: Use review or dry-run modes first, inspect generated content and reports, and avoid production accounts during testing.

Risk: Cron, growth-reply, smoke-test, and continuous modes can trigger live public account actions.

Mitigation: Run those modes only when live scheduling, replies, tests, or continuous operation are explicitly intended.

Risk: Content generation may require API keys and includes an insecure SSL override option.

Mitigation: Use low-privilege API keys, keep secrets out of shared artifacts, and do not enable QWEN_INSECURE_SSL.

## Reference(s):

- [Hermes Agent Contract](references/hermes-agent-contract.md)
- [Hermes Operator Prompt](references/hermes-operator-prompt.md)
- [Hermes X Growth Operator Prompt](references/hermes-x-growth-operator-prompt.md)
- [ClawHub Skill Page](https://clawhub.ai/kelcey2023/skills/zeelin-social-autopublisher)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance]

**Output Format:** [Markdown instructions with bash commands and JSON run artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review and dry-run modes can produce content, report, summary, and materials JSON files before live publishing.]

## Skill Version(s):

0.6.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
