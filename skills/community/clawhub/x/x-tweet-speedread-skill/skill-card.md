## Description:

X Tweet Speedread produces an instant English brief for an X post after a SkillPay charge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huangkefeng-ai](https://clawhub.ai/user/huangkefeng-ai)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to summarize public X posts into a short English speedread with key bullets, a core takeaway, risks, and suggested actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill ships an exposed billing key.

Mitigation: Remove and rotate the billing key before use, and require deployment-specific secrets from the runtime environment.

Risk: The skill sends post or user identifiers to external services while charging before summarization.

Mitigation: Disclose third-party fetch and billing providers, validate user consent, and restrict billing calls to the intended HTTPS provider.

Risk: The runtime can make unbounded network requests and accepts arbitrary direct fetch targets.

Mitigation: Enforce X status URL validation and remove arbitrary direct fetching before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huangkefeng-ai/skills/x-tweet-speedread-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/huangkefeng-ai)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON containing an English summary, key bullets, a core takeaway, risks, actions, and billing or fetch error details when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an X status URL and optionally a user identifier; may return PAYMENT_URL and PAYMENT_INFO when balance is insufficient.]

## Skill Version(s):

1.2.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
