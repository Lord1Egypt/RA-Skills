## Description:

Remote API client for TCM dietary therapy and syndrome differentiation that sends health-related queries over HTTPS to api.tcmplate.com for pattern diagnosis, ingredient lookup, food therapy plans, and tea recipes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanqubing](https://clawhub.ai/user/fanqubing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to call a hosted TCM dietary therapy service for syndrome differentiation, knowledge search, food therapy recommendations, and tea recipes. It is for informational wellness reference and should not be used as medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Health-related symptoms, disease names, constitution types, or ingredient searches are transmitted to a remote API, and the security review says the privacy documentation overstates client-side removal of personal identifiers.

Mitigation: Review before installing when personal or medical details may be entered, and remove names, phone numbers, addresses, IDs, and other identifiers from symptoms or search keywords before use.

Risk: The skill returns TCM dietary and syndrome-differentiation guidance that could be mistaken for medical advice.

Mitigation: Use outputs only as informational wellness reference and consult a licensed medical practitioner for health concerns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fanqubing/skills/tcm-dietary-api)
- [TCMPlate API documentation](https://tcmplate.com/docs)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Guidance]

**Output Format:** [JSON API responses with optional Markdown, Python, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote HTTPS API client; free tier is documented as 10 calls per day by IP, with optional paid API key use.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
