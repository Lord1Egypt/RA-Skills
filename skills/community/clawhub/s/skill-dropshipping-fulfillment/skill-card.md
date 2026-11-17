## Description:

Automates order fulfillment by pushing WooCommerce orders to CJ Dropshipping, including fetching Processing orders, matching line items to CJ variants, submitting orders to CJ, updating WooCommerce order status, logging results, and supporting dry-run and single-order modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

ISC

## Use Case:

Store operators and automation agents use this skill to turn WooCommerce Processing orders into CJ Dropshipping fulfillment requests, maintain supplier variant mappings, and record order outcomes for manual review when items cannot be matched.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place supplier orders, update WooCommerce order state, and add order notes.

Mitigation: Review scripts before installation, use dry-run and single-order modes first, and require least-privilege WooCommerce and CJ credentials for live runs.

Risk: The skill stores CJ access tokens and commerce credentials in local JSON configuration files.

Mitigation: Protect credential files with local access controls, use test or least-privilege credentials where possible, and rotate credentials after testing or suspected exposure.

Risk: Console output and JSON logs can contain customer shipping and contact data.

Mitigation: Restrict log access, redact customer data before sharing logs, and review retention for fulfillment and rejection log files.

Risk: Configured API URLs and live order payloads affect production commerce behavior.

Mitigation: Validate WooCommerce and CJ base URLs, inspect payloads during dry runs, and confirm production settings before live fulfillment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-dropshipping-fulfillment)
- [CJ Dropshipping API endpoint](https://developers.cjdropshipping.com/api2.0/v1)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces console summaries plus JSON fulfillment and rejection logs when the bundled scripts run.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
