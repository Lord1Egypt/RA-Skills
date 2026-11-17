## Description:

Helps an agent use UAPI's Answer Book endpoint, confirm the required question parameter, and explain request behavior and response codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuakami](https://clawhub.ai/user/shuakami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when a user asks for an Answer Book-style random answer via UAPI. It guides parameter collection for the required question field and points to the endpoint behavior, authentication notes, and response codes before calling the service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A generic trigger such as 'ask' could invoke the API unintentionally.

Mitigation: Narrow activation to more specific phrases such as '答案之书' or 'answerbook ask'.

Risk: Questions sent through the skill may be transmitted to the UAPI service.

Mitigation: Avoid sending sensitive questions and provide a UAPI key only when intentionally using that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuakami/skills/uapi-get-answerbook-ask)
- [UAPI base URL](https://uapis.cn/api/v1)
- [UAPI website](https://uapis.cn)
- [Quick start](references/quick-start.md)
- [Answer Book operation](references/operations/get-answerbook-ask.md)
- [Random resource category](references/resources/Random.md)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Markdown]

**Output Format:** [Markdown guidance with endpoint details and optional API call preparation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May transmit the user's question to the UAPI service; an optional UAPI key should only be used deliberately for that service.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
