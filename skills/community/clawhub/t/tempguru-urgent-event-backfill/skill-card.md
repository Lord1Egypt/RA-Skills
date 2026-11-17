## Description:

Helps an agent triage urgent event staffing gaps, assess rush timing, and guide a buyer through TempGuru’s quote handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kissmyabs32](https://clawhub.ai/user/kissmyabs32)

### License/Terms of Use:

MIT-0

## Use Case:

External event organizers use this skill to respond to same-week or day-of staffing shortfalls in the United States and Canada. It gathers event requirements, checks rush guidance, and prepares a quote handoff for the buyer to submit.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Event details sent to TempGuru may be retained without advance disclosure to the user.

Mitigation: Tell the user before sending event details to TempGuru, and keep contact information out of MCP calls so the buyer can enter it on the form.

Risk: The security scan had partial coverage because one local reference could not be resolved.

Mitigation: Review the supplied package and resolve the missing local reference before relying on the skill.

## Reference(s):

- [TempGuru AI agent documentation](https://tempguru.co/ai-agents)
- [TempGuru staffing MCP service](https://mcp.tempguru.co/mcp)
- [TempGuru staffing request form](https://tempguru.co/get-staffing?utm_source=ai-agent&utm_medium=skill)
- [TempGuru Event Staffing Planner GPT](https://chatgpt.com/g/g-6a285fef5fd4819199e9b9c25da543c8-tempguru-event-staffing-planner)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text, Links]

**Output Format:** [Conversational guidance with staffing estimates, rush status, and buyer-operated quote handoff links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Planning estimates and lead-time guidance are not reservations or guarantees; the buyer submits the quote form personally.]

## Skill Version(s):

1.7.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
