## Description:

Queries company business registration information by company name or unified social credit code using TianAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up Chinese business registration details such as legal representative, registered capital, establishment date, address, business scope, company status, and unified social credit code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed through command-line arguments, plaintext .env files, or URL query parameters.

Mitigation: Provide TIANAPI_COMPANY_KEY through the runtime environment or a secret manager, avoid passing keys in commands, and avoid storing keys in scripts/.env.

Risk: Company lookup targets and related query data are sent to TianAPI.

Mitigation: Use a dedicated low-privilege TianAPI key where available and avoid querying confidential company targets unless disclosure to TianAPI is acceptable.

Risk: The server security verdict is suspicious.

Mitigation: Review the skill before installing and scan it before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-company-info)
- [TianAPI company information API](https://www.tianapi.com/apiview/272)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TIANAPI_COMPANY_KEY credential.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
