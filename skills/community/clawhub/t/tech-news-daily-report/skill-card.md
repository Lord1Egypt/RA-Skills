## Description:

Generates a daily technology and AI news report with recent-search sourcing, relevance and recommendation scores, deduplication, topic mapping, local Markdown output, Feishu document creation, and Feishu group delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binhuatochina](https://clawhub.ai/user/binhuatochina)

### License/Terms of Use:

MIT-0

## Use Case:

External users and knowledge workers use this skill to collect recent technology and AI news, rank and summarize key items, and publish a daily report to local Markdown and Feishu. It is suited for routine news monitoring where the configured Feishu destination is intentional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill mandates sending generated reports to a fixed embedded Feishu group, which can expose private or organization-specific report content if used without confirming the destination.

Mitigation: Use only when that Feishu group is the intended recipient, or replace the embedded destination with a user-selected confirmed target and make external sending optional.

## Reference(s):

- [Feishu document operation reference](references/feishu-doc.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, configuration, guidance]

**Output Format:** [Markdown report with scored news items, topic relationship map, source links, data summary, local file path, and Feishu sync record.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may create local files under memory/ and publish the report to Feishu when the required integrations are available.]

## Skill Version(s):

0.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
