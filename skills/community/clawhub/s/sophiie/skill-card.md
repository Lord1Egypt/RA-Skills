## Description:

Manage your Sophiie sales pipeline - leads, inquiries, appointments, FAQs, policies, SMS, and calls via the Sophiie REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomc98](https://clawhub.ai/user/tomc98)

### License/Terms of Use:


## Use Case:

Sales and operations teams use this skill through an OpenClaw-compatible agent to inspect and manage Sophiie leads, inquiries, appointments, FAQs, policies, outbound SMS, and outbound calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A production API key may allow the skill to send real SMS messages or calls and change customer or business records.

Mitigation: Use a least-privilege or sandbox Sophiie API key where possible, and require human confirmation before sending SMS or calls or changing/deleting leads, FAQs, and policies.

Risk: The skill can access live sales pipeline and organization data through the Sophiie API.

Mitigation: Limit access to workspaces and API keys that are appropriate for the user, and avoid sharing sensitive API responses outside the intended agent session.

## Reference(s):

- [Sophiie Documentation](https://docs.sophiie.ai)
- [Sophiie API Reference](https://docs.sophiie.ai/api)
- [ClawHub Skill Page](https://clawhub.ai/tomc98/skills/sophiie)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SOPHIIE_API_KEY plus curl and jq; list endpoints are paginated and default to 50 items per page.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
