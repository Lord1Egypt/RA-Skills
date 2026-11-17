## Description:

公司一页纸摸底（行情+身份+估值成长）。深度研读/备忘请走 Role；全行业比价走 wm-industry-members。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerryzhou](https://clawhub.ai/user/jerryzhou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve a concise Chinese-language company or stock snapshot covering quote, identity, valuation, growth, quality, shareholder data, freshness, and deeplinks. It supports single-symbol and batch company-card lookups for quick market and fundamentals triage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be implicitly invoked for matching finance questions.

Mitigation: Review the installation context and invocation policy so users understand when company or stock snapshots may be returned.

Risk: Returned market and fundamentals data can be incomplete, stale, or unsuitable as standalone investment advice.

Mitigation: Use the returned freshness fields and deeplinks, preserve cited source skill output for key numbers, and route deeper analysis to the documented follow-up skills or roles.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jerryzhou/skills/wm-company-card)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [JSON skill-run response with markdown deeplinks and agent-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single symbol or up to 50 symbols and selectable include modules such as quote, kline, identity, valuation, growth, quality, and shareholder.]

## Skill Version(s):

1.2.9 (source: frontmatter, manifest, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
