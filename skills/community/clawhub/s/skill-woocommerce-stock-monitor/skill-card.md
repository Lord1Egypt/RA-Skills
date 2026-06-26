## Description: <br>
Monitor WooCommerce products for out-of-stock changes and send Telegram alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and store operators use this skill to monitor WooCommerce product inventory, detect newly out-of-stock items, and send Telegram notifications to a configured chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product names, SKUs, and out-of-stock details are sent to the configured Telegram chat. <br>
Mitigation: Use the skill only when that disclosure is acceptable, confirm the chat ID before scheduling, and restrict Telegram bot token access. <br>
Risk: WooCommerce credentials are required to fetch product inventory. <br>
Mitigation: Use a read-only WooCommerce API key, store credentials outside the skill files, and keep the WooCommerce URL on HTTPS. <br>
Risk: Scheduled monitoring may continue after it is no longer needed. <br>
Mitigation: Review cron entries periodically and remove the scheduled job when inventory monitoring is retired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-woocommerce-stock-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JavaScript console output, Telegram alert messages, and JSON state file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, WooCommerce REST API credentials, and optional Telegram bot configuration.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter and _meta.json report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
