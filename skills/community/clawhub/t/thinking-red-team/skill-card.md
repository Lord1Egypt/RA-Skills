## Description:

For authorized security review of code, auth, or APIs you control, model the attacker, map the attack surface, and report only findings with a reproducible exploit path and verified mitigation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to run authorized adversarial reviews of code, authentication, authorization, APIs, data handling, or infrastructure. It helps produce only reproducible security findings with concrete exploit paths, mitigation steps, and re-test criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended for adversarial security review and could be misapplied to systems without authorization.

Mitigation: Use it only for systems you own or have explicit permission to test, and confirm target, scope, success condition, and stop rules before probing.

Risk: Security reports can overstate scanner leads or speculative weaknesses as findings.

Mitigation: Keep only findings with a concrete entry point, ordered exploit steps, realized impact, and re-test guidance; drop incomplete paths.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown security review report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are limited to complete exploit paths with entry point, ordered steps, realized impact, bypass attempts, mitigation, and re-test guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
