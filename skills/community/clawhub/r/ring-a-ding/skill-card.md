## Description:

Ring-a-Ding lets an agent place AI phone calls in the US and Canada to call businesses, schedule or cancel appointments, run hands-free user conversations, and return transcripts, summaries, and structured extraction results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vlbeta](https://clawhub.ai/user/vlbeta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use Ring-a-Ding to make real phone calls for scheduling, reservations, customer-service follow-up, voicemail, and phone-first working sessions. It is intended for US and Canadian calls and returns call status, transcript, summary, and optional extracted data.

### Deployment Geography for Use:

United States and Canada

## Known Risks and Mitigations:

Risk: Phone calls and call context can expose sensitive personal, health, payment, insurance, address, or account details to an external service.

Mitigation: Provide only the minimum call context needed for the task and avoid unnecessary sensitive details.

Risk: The npm-installed CLI and external service influence call behavior and receive call data.

Mitigation: Review the skill before installing, run it in a restricted environment, and provide only the required RAD_API_KEY and OPENAI_API_KEY credentials.

Risk: Scheduled polling jobs can continue waking the agent after a call if they are not removed.

Mitigation: Create polling jobs only for the intended call and remove them when the call reaches a terminal status.

Risk: The skill only supports US and Canadian phone numbers.

Mitigation: Confirm the destination is an E.164 +1 number before dialing and decline unsupported international calls up front.

## Reference(s):

- [Ring-a-Ding documentation](https://ringading.ai/docs)
- [Ring-a-Ding OpenClaw quick-start](https://ringading.ai/openclaw)
- [ClawHub skill page](https://clawhub.ai/vlbeta/skills/ring-a-ding)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces call setup instructions and describes JSON call results including status, transcript, summary, and optional extracted data.]

## Skill Version(s):

0.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
