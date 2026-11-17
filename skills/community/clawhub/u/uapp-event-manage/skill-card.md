## Description:

Helps agents manage Umeng custom event definitions through `umeng-cli call`, including App event creation, Mini Program batch event creation, and App or Mini Program event-list checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[squall0925](https://clawhub.ai/user/squall0925)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to create, batch-create, precheck, and verify Umeng custom event definitions for App, Mini Program, H5, and mini-game properties.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags opaque telemetry involving app identifiers.

Mitigation: Treat appkey and dataSourceId values as sensitive tenant identifiers and avoid exposing them in telemetry unless the user and deployment policy explicitly allow it.

Risk: The security evidence flags the curl-to-shell installer as unsafe.

Mitigation: Prefer the documented npm install path and use the curl-to-shell installer only after independent review.

Risk: The skill can create event definitions that are documented as irreversible.

Mitigation: Require local parameter validation, duplicate prechecks, and explicit user confirmation before any write operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/squall0925/skills/uapp-event-manage)
- [umeng-cli project homepage](https://github.com/umeng/umeng-cli)
- [Umeng OpenAPI gateway](https://gateway.open.umeng.com/openapi)
- [Publisher profile](https://clawhub.ai/user/squall0925)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON command arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose read or write Umeng OpenAPI calls; write operations require user confirmation and local parameter validation.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
