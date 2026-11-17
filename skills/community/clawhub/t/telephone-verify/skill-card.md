## Description:

Verifies whether a Chinese mobile phone number, real name, and ID card number match through Juhe telecom real-name authentication and can return carrier, province, and city information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xwzgit](https://clawhub.ai/user/xwzgit)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check lawful, consented telecom identity verification for a Chinese phone number, real name, and ID card number. It is intended for workflows that need a concise match result plus optional carrier and location details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive identity data and the Juhe API key may appear in request URLs or terminal logs.

Mitigation: Use only lawful, consented verification workflows; prefer POST bodies, mask output and logs by default, and confirm before sending identity data to Juhe.

Risk: The security evidence says third-party data sharing is under-disclosed.

Mitigation: Review Juhe's data handling terms and disclose third-party processing before deploying the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xwzgit/skills/telephone-verify)
- [Juhe API reference](references/api.md)
- [Juhe website](https://www.juhe.cn/)
- [Juhe telecom query endpoint](https://v.juhe.cn/telecom/query)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Markdown guidance and command-line output, with optional JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Juhe API key and user-provided mobile number, real name, and ID card number.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
