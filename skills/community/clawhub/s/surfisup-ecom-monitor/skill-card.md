## Description:

Provides daily Shopify sales summaries, low stock alerts, and competitor price tracking using a user-provided Shopify API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamod](https://clawhub.ai/user/jamod)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and developers use this skill to have an agent summarize Shopify sales, flag low inventory, and monitor competitor prices from user-provided Shopify access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to create a recurring cron job that keeps accessing Shopify data, despite documentation claiming no scheduling or persistence.

Mitigation: Install only when recurring monitoring is intended, inspect and remove scheduled tasks when no longer needed, and review generated commands before execution.

Risk: Shopify API access and notification destinations could expose store data if permissions or recipients are too broad.

Mitigation: Use a Shopify API key restricted to read-only minimum scopes and verify where email or Telegram reports are sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamod/skills/surfisup-ecom-monitor)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact README](artifact/README.md)
- [Artifact changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text reports and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve user-provided Shopify API access and notification destinations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
