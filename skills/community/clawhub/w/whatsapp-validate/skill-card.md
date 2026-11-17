## Description:

Check if phone numbers exist in the local Baileys session cache.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators working with OpenClaw WhatsApp/Baileys sessions use this skill to check one or more phone numbers against the local cache and optionally list cached WhatsApp identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw WhatsApp/Baileys cache data and may print full phone numbers and JIDs.

Mitigation: Run it only in sessions where exposing cached contact identifiers is acceptable, and avoid the list command unless you intend to disclose those identifiers.

Risk: A number not found in the cache is not proof that the number lacks WhatsApp.

Mitigation: Treat unknown results as cache misses and avoid using them as definitive account-existence decisions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON responses and concise Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads the local OpenClaw WhatsApp/Baileys cache and reports cached phone numbers, JIDs, and known/unknown status.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
