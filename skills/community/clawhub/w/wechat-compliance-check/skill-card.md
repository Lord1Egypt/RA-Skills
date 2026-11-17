## Description:

Checks WeChat public-account articles for sensitive compliance terms, reports matched risks, and can rewrite text into safer phrasing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT-0

## Use Case:

Content authors and editors use this skill before publishing WeChat public-account articles to detect risky terms, generate a compliance report, and prepare safer wording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested replacements may change nuance or produce misleading wording in political, technical, medical, or commercial content.

Mitigation: Review the compliance report and rewritten text before publishing.

Risk: Fix mode can modify the input article file.

Mitigation: Use report-only mode when no file changes are desired, or review the timestamped backup before accepting edits.

## Reference(s):

- [Sensitive words reference](references/sensitive-words.md)
- [Project homepage](https://github.com/nicekate/wechat-compliance-check)
- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/wechat-compliance-check)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown compliance report with rewritten text or replacement guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May modify the target file and create a timestamped backup in fix mode; report-only mode avoids file changes.]

## Skill Version(s):

1.0.2 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
