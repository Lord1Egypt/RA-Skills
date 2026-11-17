## Description:

Read Workvivo feeds, news, posts, spaces, events, people, notifications, and search through the user's signed-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Employees use this skill to review their organization's Workvivo updates, find internal information, and look up colleagues, spaces, and events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Network access was detected without a declared tool scope, and broad activation wording may lead to use outside a clearly scoped Workvivo request.

Mitigation: Invoke the skill for explicit Workvivo information requests and confirm the paired signed-in account is appropriate for the requested data.

Risk: Workvivo responses can include personal details and sensitive values such as account tokens or event passwords.

Mitigation: Return only fields needed for the request and exclude credentials, contact details, and event passwords.

## Reference(s):

- [Workvivo Read Endpoints](references/endpoints.md)
- [Workvivo Fpx on ClawHub](https://clawhub.ai/chrischall/skills/workvivo-fpx)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Workvivo content returned as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only retrieved content, projected to fields relevant to the request.]

## Skill Version(s):

0.5.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
