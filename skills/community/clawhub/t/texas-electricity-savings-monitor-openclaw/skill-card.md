## Description:

Guides Texas residential electricity shoppers through address confirmation, usage estimation, plan recommendation, self-service plan routing, and daily or weekly savings monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[catkennel](https://clawhub.ai/user/catkennel)

### License/Terms of Use:

MIT-0

## Use Case:

External Texas residential electricity consumers use this skill to confirm a service address, compare current plan options, open the matching Personalized Energy address page, and set daily or weekly savings monitoring.

### Deployment Geography for Use:

United States (Texas)

## Known Risks and Mitigations:

Risk: Residential service address and usage-related information is sent to Personalized Energy or PowerLego services for plan lookup.

Mitigation: Install only with clear user-facing privacy disclosure and collect only the address and usage details needed for the requested electricity workflow.

Risk: The release ships an exposed bearer token for the external PowerLego service.

Mitigation: Rotate and remove the exposed token before deployment, and move authentication behind a protected service or secret store.

Risk: Plan availability, rates, and estimated savings can change and should not be presented as guaranteed.

Mitigation: Present plan results as current lookup guidance, route users to the Personalized Energy address page for live review, and avoid guaranteed-savings claims.

## Reference(s):

- [Address Completeness](references/address-completeness.md)
- [Intent Routing](references/intent-routing.md)
- [OpenClaw Execution Guide](references/openclaw-execution.md)
- [Response Strategy](references/response-strategy.md)
- [Personalized Energy Texas Electricity Rates](https://www.personalized.energy/electricity-rates/texas)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Consumer-facing text or Markdown with numbered address and plan lists, URLs, and supporting JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include confirmed addresses, ESIID values when available, estimated usage summaries, top plan lists, best-plan recommendations, Personalized Energy address URLs, and monitoring recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
