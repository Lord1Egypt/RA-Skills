## Description: <br>
High-ticket lead qualification agent for realtors and property managers that handles inbound Zillow/Realtor.com inquiries, qualifies budget and timeline, schedules viewings, and uses ThumbGate guardrails for Fair Housing safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorganapolsky](https://clawhub.ai/user/igorganapolsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External realtors and property managers use this agent to respond to inbound property portal leads, check pre-approval, budget, and move-in timing, and schedule qualified viewings. It is intended for commercial lead handling workflows where human operators configure calendars, lead sources, document handling, and Fair Housing guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may automate customer replies and viewing bookings across lead sources and calendars without enough clear operational controls. <br>
Mitigation: Use limited-permission lead source and calendar accounts, start with human approval for replies and bookings, and confirm exactly which systems the agent can access before deployment. <br>
Risk: The skill handles pre-approval PDF uploads, which can contain sensitive financial or personal information. <br>
Mitigation: Define where pre-approval documents are stored, who can access them, retention periods, and deletion procedures before enabling the workflow. <br>
Risk: Fair Housing safety claims depend on correct ThumbGate setup and may fail if the rules are not active or tested. <br>
Mitigation: Verify ThumbGate rules before relying on the skill and test blocked topics such as neighborhood safety, schools, and demographics before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/igorganapolsky/real-estate-lead-qualifier) <br>
- [Twilio](https://twilio.com) <br>
- [Calendly](https://calendly.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with setup steps, policy rules, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent operating guidance for lead responses, qualification checks, calendar booking, and Fair Housing guardrail setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
