## Description:

Test whether an HTTP endpoint enforces rate limiting by sending a burst of requests and checking for 429 responses, Retry-After, and X-RateLimit headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techris93](https://clawhub.ai/user/techris93)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to validate that an API, gateway, or middleware deployment throttles burst traffic before production release or during authorized service audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Burst testing endpoints without authorization can create unwanted traffic or violate service policies.

Mitigation: Run the skill only against endpoints the user is authorized to test and coordinate test volume with the service owner.

Risk: The included shell script uses a PID-based temporary file path, which is unsafe on shared or privileged systems.

Mitigation: Replace the temporary file path with mktemp before regular use and avoid elevated privileges.

## Reference(s):

- [OpenClaw threat model](https://github.com/openclaw/trust)
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and an authorized HTTP endpoint target.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
