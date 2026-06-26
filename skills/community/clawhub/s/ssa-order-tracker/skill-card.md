## Description: <br>
Track and manage sales orders with status updates, notifications, and dashboard reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cjboy007](https://clawhub.ai/user/cjboy007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations and sales staff use this skill to maintain local order records, update fulfillment status, review dashboard summaries, and prepare customer order-status emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores order and customer data in local JSON files, logs, and backups. <br>
Mitigation: Use it only with order data approved for local storage, remove bundled sample customer data before production use, and manage local backups and logs according to the user's data-retention policy. <br>
Risk: The notification script can send customer emails through the configured SMTP account. <br>
Mitigation: Run dry-runs first, verify recipients and message content, and use a dedicated sender credential for this skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cjboy007/ssa-order-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/cjboy007) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and local file guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local order status updates, dashboard summaries, notification drafts or sends, logs, and JSON data changes depending on the invoked script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
