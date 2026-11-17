## Description:

Gets real-time and scheduled bus arrival times for TPER buses in Bologna and Ferrara, Italy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lore2601](https://clawhub.ai/user/lore2601)

### License/Terms of Use:


## Use Case:

Transit riders and agents assisting them use this skill to check TPER bus arrivals for Bologna or Ferrara when the request includes a numeric stop code and line number. It supports real-time arrivals when no time is provided and scheduled arrival lookups when a time is provided.

### Deployment Geography for Use:

Italy (Bologna and Ferrara transit use cases)

## Known Risks and Mitigations:

Risk: Transit query details, including stop code, line number, and optional time, are sent to TPER's Hellobus service.

Mitigation: Use the skill only for clear TPER transit requests and avoid adding unrelated personal data to the query.

Risk: Ambiguous bus questions may target the wrong transit system, stop, or line.

Mitigation: Ask for confirmation when the user has not provided TPER context, a numeric stop code, and a numeric line number.

Risk: Arrival results depend on external Hellobus API availability and the validity of the provided stop and line combination.

Mitigation: Report API failures or empty results clearly and suggest checking the stop code and line number or trying again later.

## Reference(s):

- [TPER Hellobus API endpoint](https://hellobuswsweb.tper.it/web-services/hellobus.asmx/QueryHellobus)
- [ClawHub skill page](https://clawhub.ai/lore2601/skills/tper-hellobus-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with bullet-listed bus arrivals and optional shell command or API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access to hellobuswsweb.tper.it plus numeric stop code and line number inputs.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
