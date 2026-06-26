## Description: <br>
Track service history, maintenance schedules, mechanics, registration, insurance, and admin for all your vehicles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris-openclaw](https://clawhub.ai/user/chris-openclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to maintain records for cars, trucks, motorcycles, boats, RVs, and trailers, including service history, maintenance schedules, mechanic contacts, costs, and administrative deadlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores vehicle and ownership records locally, which may include sensitive details such as VINs, plate numbers, policy information, or loan details. <br>
Mitigation: Only store sensitive identifiers when needed, keep vehicle-data.json in a trusted local environment, and periodically remove records that are no longer needed. <br>
Risk: Maintenance schedules and proactive reminders may be incomplete or unsuitable for a specific vehicle, usage pattern, or manufacturer requirement. <br>
Mitigation: Treat suggested intervals as adjustable defaults and confirm critical maintenance decisions against the owner's manual or a qualified mechanic. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris-openclaw/vehicle-os) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Conversational Markdown with structured vehicle records and maintenance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists vehicle ownership and service data in local vehicle-data.json when used by a compatible agent.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
