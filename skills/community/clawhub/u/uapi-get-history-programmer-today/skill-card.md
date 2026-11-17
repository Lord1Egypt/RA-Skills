## Description:

Calls UAPI's GET /history/programmer/today endpoint to retrieve programmer and computer-science events that happened on today's date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks for programmer-history-on-this-day facts and needs the correct UAPI endpoint, authentication posture, response codes, and call guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad English trigger "today" could route unrelated date requests to this skill.

Mitigation: Confirm the user specifically wants programmer-history-on-this-day information before invoking the UAPI endpoint.

Risk: Using the endpoint contacts uapis.cn, and anonymous quota may be exhausted or require a UAPI key.

Mitigation: Disclose external API use where appropriate and request or configure a UAPI key only when the service requires it.

## Reference(s):

- [GET /history/programmer/today operation](references/operations/get-history-programmer-today.md)
- [Quick start](references/quick-start.md)
- [Misc category reference](references/resources/Misc.md)
- [UAPI base endpoint](https://uapis.cn/api/v1)
- [ClawHub skill page](https://clawhub.ai/shuakami/skills/uapi-get-history-programmer-today)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with endpoint, authentication, and response-code details; may include API call instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No request parameters are documented for the endpoint; anonymous use may hit quota and require a UAPI key.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
