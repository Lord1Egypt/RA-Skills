## Description:

Volcano helps agents summarize non-sensitive public or user-visible Volcengine product, pricing, billing, and service announcement information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect concise summaries of visible Volcengine product specifications, pricing links, billing overviews, cost trends, and service announcements without performing account operations or API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing or console summaries may expose account IDs, keys, or other sensitive details if copied from user-visible pages.

Mitigation: Keep console work user-directed, do not provide credentials to the agent, and review generated summaries before storing or sharing them.

Risk: Automated access to console pages could exceed the skill's stated boundary of visible summaries and drift into account operations.

Mitigation: Use the skill only for visible information summaries and avoid account changes, permission changes, paid API calls, or credential handling.

## Reference(s):

- [ClawHub Volcano Skill](https://clawhub.ai/mikeclaw007/skills/volcano)
- [Volcengine Homepage](https://www.volcengine.com/)
- [Volcengine Console](https://console.volcengine.com/)
- [Volcengine Documentation](https://www.volcengine.com/docs)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries with source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should stay within visible, non-sensitive information and avoid copying credentials, account IDs, or keys.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
