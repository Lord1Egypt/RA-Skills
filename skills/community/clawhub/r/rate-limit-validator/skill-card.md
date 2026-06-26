## Description: <br>
Test whether an HTTP endpoint enforces rate limiting by sending a burst of requests and checking for HTTP 429 responses, Retry-After headers, and X-RateLimit headers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Techris93](https://clawhub.ai/user/Techris93) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to validate whether APIs, gateways, or middleware enforce rate limits before production release or after hardening changes. It can also support authorized audits of services that depend on throttling behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bursting HTTP GET requests against an endpoint can disrupt a service or violate acceptable-use rules if the target is not authorized. <br>
Mitigation: Run the skill only against owned or explicitly authorized endpoints, and keep the request count appropriate for the environment. <br>
Risk: Rate-limit validation can be mistaken for a security boundary check that proves broader application safety. <br>
Mitigation: Treat the result as evidence about throttling behavior only, and review other security controls separately. <br>


## Reference(s): <br>
- [Rate Limit Validator on ClawHub](https://clawhub.ai/Techris93/rate-limit-validator) <br>
- [OpenClaw threat model](https://github.com/openclaw/trust) <br>
- [OpenClaw security policy](https://github.com/openclaw/openclaw/security/policy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Analysis] <br>
**Output Format:** [Markdown with inline bash code blocks and concise test result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and sends repeated HTTP GET requests to the target endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
