## Description:

Monitor WooCommerce products for out-of-stock changes and send Telegram alerts. Run daily via cron.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and developers use this skill to run scheduled inventory checks against WooCommerce, detect products newly out of stock, and send Telegram alerts to an operations chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WooCommerce API credentials can be sent over plaintext HTTP if the store URL is configured with an insecure URL.

Mitigation: Use only an HTTPS WooCommerce store URL and avoid scheduling the cron job until HTTPS enforcement is added.

Risk: The skill depends on WooCommerce and Telegram credentials for automated execution.

Mitigation: Use a read-only WooCommerce API key, protect the credentials file, and keep Telegram token and chat ID outside source-controlled files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-woocommerce-stock-monitor)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js, WooCommerce read-only API credentials, Telegram bot credentials, and a local state file for prior stock status.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact files report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
