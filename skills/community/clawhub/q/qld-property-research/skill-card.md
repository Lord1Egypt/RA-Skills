## Description:

Detailed Queensland property due-diligence for a single street address using official sources only. Use when an agent needs to research a Queensland property beyond listing basics, including flood-map checks, nearest train-station access, main-road proximity, or a structured property report with cited findings and a composite suitability score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhear22](https://clawhub.ai/user/mhear22)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to screen one Queensland property address at a time for NBN technology, flood-map status, main-road proximity, train-station walking access, and a composite suitability score. It is intended for structured due-diligence reporting with concise citations and clear unsupported-data handling.

### Deployment Geography for Use:

Australia (Queensland)

## Known Risks and Mitigations:

Risk: Property addresses and route coordinates may be sent to Queensland government or council services, NBN Co, and openrouteservice.

Mitigation: Use the skill only for addresses you are comfortable checking through those services, and avoid submitting sensitive location data unless the user accepts that disclosure.

Risk: openrouteservice requires an API key for walking-route checks.

Mitigation: Keep ORS_API_KEY in the runtime environment and do not hard-code it in skill files, reports, or shared prompts.

Risk: The report is a screening aid and may not capture legal, engineering, insurance, accessibility, or flood-risk nuances.

Mitigation: Present findings with the skill's caveats, cite the official sources used, mark unsupported sections clearly, and direct users to qualified professional review for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mhear22/skills/qld-property-research)
- [QLD Property Research Methodology](references/methodology.md)
- [QLD Property Research Official Sources](references/official-sources.md)
- [openrouteservice Routing](references/openrouteservice.md)
- [Find addresses | Queensland Government](https://www.qld.gov.au/environment/land/title/addressing/finding)
- [Using the Queensland Globe | Business Queensland](https://www.business.qld.gov.au/running-business/support-services/mapping-data-imagery/queensland-globe/using)
- [Plan your journey | Translink](https://translink.com.au/plan-your-journey)
- [Check address | nbn](https://www.nbnco.com.au/check-address)
- [openrouteservice API](https://api.openrouteservice.org/)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Structured Markdown report with cited findings, section scores, and optional helper-script JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires one full Queensland street address; uses ORS_API_KEY for openrouteservice walking-route checks when configured.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
