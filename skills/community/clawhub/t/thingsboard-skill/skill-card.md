## Description:

Manage ThingsBoard devices, dashboards, telemetry, and users via the ThingsBoard REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoangnv170752](https://clawhub.ai/user/hoangnv170752)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to manage ThingsBoard IoT resources through REST API workflows, including device, telemetry, dashboard, asset, customer, and user operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact ships default ThingsBoard credentials.

Mitigation: Replace bundled credentials with unique least-privilege credentials and avoid committing credentials.json.

Risk: The skill includes high-impact ThingsBoard operations such as deleting telemetry and making dashboards public.

Mitigation: Require explicit confirmation before destructive telemetry changes or public dashboard exposure.

Risk: The skill can authenticate to local or remote ThingsBoard servers using user-provided credentials.

Mitigation: Use it only against ThingsBoard servers you control and use HTTPS for any non-local server.

## Reference(s):

- [ThingsBoard](https://thingsboard.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, TB_URL, TB_USERNAME, and TB_PASSWORD.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
