## Description:

Automatically segments OKKI CRM customers into VIP, active, normal, dormant, and lost groups, generates lifecycle and value-based strategy recommendations, and can sync prefixed segment tags back to OKKI CRM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, customer success, and CRM operations teams use this skill through an agent to collect OKKI CRM customer activity, score customer value and lifecycle status, generate strategy recommendations, and prepare or apply segment tag updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CRM credentials, token cache, customer data, logs, backups, and generated reports may be stored in plaintext on local disk.

Mitigation: Use least-privilege OKKI credentials and protect or encrypt .env files, token cache, generated data, logs, backups, and reports before running against real customer data.

Risk: The OKKI API destination is read from external configuration and may point at unintended endpoints.

Mitigation: Review config.json before execution and allow only the intended HTTPS OKKI endpoints.

Risk: Confirmed tag sync can update CRM customer tags in bulk.

Mitigation: Run tag sync in dry-run first, verify the planned SEG: tag changes, then use --limit or --customer before any broad --confirm operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/ssa-customer-segmentation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands, console summaries, and JSON file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local customer data, scoring, strategy, log, backup, and tag-sync report JSON files; OKKI tag sync is dry-run unless confirmed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
