## Description:

Decide whether OpenClaw should send a spontaneous casual message during periodic checks, and when it should, choose a natural interaction type plus concise guidance for how to deliver it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fjrevoredo](https://clawhub.ai/user/fjrevoredo)

### License/Terms of Use:


## Use Case:

OpenClaw users and integrators use this skill to decide whether a scheduled check should become a casual proactive message, and to select concise message guidance when outreach is appropriate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enable automated proactive messages that use personal context without clear consent, rate limits, or transparency.

Mitigation: Deploy it only with explicit opt-in, clear user-visible behavior, quiet hours, rate limits, and permission checks for each data source.

Risk: Data-aware interaction types may involve calendar, smart-home, traffic, weather, news, market, or other personal integrations.

Mitigation: Use only authorized, fresh, and relevant data; when reliable context is unavailable, keep the message general or skip the data-aware interaction.

Risk: Spontaneous outreach can feel intrusive if it is too frequent or framed as an alert.

Mitigation: Keep messages brief, low-pressure, and easy to ignore, and enforce separate quiet-hour and frequency controls in the OpenClaw setup.

## Reference(s):

- [OpenClaw Skills Documentation](https://docs.openclaw.ai/tools/skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions and JSON output contract]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The runtime helper emits JSON with a required decision field; when decision is yes, it also emits an interaction type and interaction description.]

## Skill Version(s):

2.0.0 (source: server evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
