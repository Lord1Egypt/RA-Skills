## Description:

Use wrk for HTTP load testing, including Lua scripting for dynamic request headers such as randomized X-Forwarded-For IPs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-montanari](https://clawhub.ai/user/felix-montanari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, run, and interpret authorized HTTP load tests with wrk, including tests that need Lua-based dynamic headers, randomized inputs, custom request bodies, or conservative scale-up guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Load tests can disrupt production, third-party, or shared services if run without authorization or with aggressive settings.

Mitigation: Confirm authorization, prefer local/dev/staging or approved performance-test environments, start with conservative wrk parameters, and scale only while monitoring service health.

Risk: Randomized X-Forwarded-For headers can bypass or distort rate limits, abuse controls, logging, attribution, caches, or dashboards.

Mitigation: Use randomized client-IP headers only when that behavior is an explicit part of an authorized test, and verify how proxies and applications process the headers.

## Reference(s):

- [wrk project](https://github.com/wg/wrk)
- [ClawHub skill page](https://clawhub.ai/felix-montanari/skills/wrk)
- [Publisher profile](https://clawhub.ai/user/felix-montanari)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash and Lua code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces commands, Lua examples, checklists, and interpretation guidance for authorized wrk load tests.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
