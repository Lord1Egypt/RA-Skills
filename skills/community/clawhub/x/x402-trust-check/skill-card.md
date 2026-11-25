## Description:

Check the trust rating of any x402 service before paying it. Free JSON, daily, sybil-resistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aladaf](https://clawhub.ai/user/aladaf)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to check an x402 service's adoption and liveness signals before deciding whether to pay, or to see whether a service is listed. The rating is a signal, not a guarantee of service quality.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Checking a service sends its hostname to the rating provider.

Mitigation: Consider whether hostname sharing is acceptable before querying; the skill uses the hostname rather than the full URL.

Risk: A rating can be mistaken for a guarantee of service quality or safety.

Mitigation: Treat adoption and liveness as limited signals and make the payment decision using the user's risk tolerance.

Risk: The security evidence has partial coverage and does not establish the destinations of some unresolved references.

Mitigation: Review referenced destinations before relying on the skill.

## Reference(s):

- [Agent Economy Report ratings](https://agenteconomy.report/s/)
- [Rating methodology and corrections](https://agenteconomy.report/s/policy)
- [Agent Economy Report data archive](https://agenteconomy.report/s/data/)
- [ClawHub release page](https://clawhub.ai/aladaf/skills/x402-trust-check)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON rating data summarized in a concise text report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ratings measure adoption and liveness, not service quality or a guarantee of safety.]

## Skill Version(s):

1.5.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
