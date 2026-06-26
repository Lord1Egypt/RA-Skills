## Description: <br>
A high-trust lead qualification and appointment booking agent for realtors that prevents MLS hallucinations via ThumbGate grounding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External real estate professionals use this skill to qualify buyer, seller, and renter leads, check requests against verified listing data, book appointments, and log lead details to a CRM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect lead contact details and behavioral scores for CRM storage. <br>
Mitigation: Disclose lead data collection and scoring where required, define retention rules, and test with non-production CRM records before live use. <br>
Risk: The skill can propose or perform calendar bookings and CRM writes. <br>
Mitigation: Require explicit confirmation before writes, use least-privilege integrations, and validate rollback or correction procedures. <br>
Risk: The skill makes Fair Housing, DNC, and zero-hallucination claims that may affect regulated real-estate workflows. <br>
Mitigation: Independently validate compliance rules, DNC checks, and listing-grounding behavior before relying on the skill in production. <br>
Risk: The artifact includes a paid upgrade link and release evidence flags purchase capability. <br>
Mitigation: Require explicit user approval before opening purchase flows or making any payment-related action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/real-estate-lead-pilot) <br>
- [Setup guide](setup-guide.md) <br>
- [ThumbGate prevention rules](thumbgate-rules.md) <br>
- [Lead Pilot Premium purchase page](https://iganapolsky.gumroad.com/l/tzehg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with lead qualification dialogue, setup commands, configuration steps, and structured CRM or calendar action guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose CRM writes, calendar bookings, lead scoring, and purchase links; these actions should be confirmed before execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
