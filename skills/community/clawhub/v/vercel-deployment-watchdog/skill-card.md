## Description:

Monitor Vercel-hosted site deployments with automated health checks, cache freshness verification, and API validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanpruss](https://clawhub.ai/user/ivanpruss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to monitor Vercel deployments they own, check homepage and API health, detect deployment changes, and configure recurring OpenClaw monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes HTTP requests from the agent environment to user-provided homepage and API URLs, and Vercel when a token is supplied.

Mitigation: Run it only against deployments you own or are authorized to monitor, and do not allow untrusted input to choose target URLs.

Risk: Security evidence says URL checks can be bypassed and may allow requests to internal or private services.

Mitigation: Avoid ALLOW_INTERNAL unless private-network monitoring is intentional and approved; review target URLs before execution.

Risk: Vercel tokens can expose deployment metadata if mishandled.

Mitigation: Use VERCEL_TOKEN from a protected environment variable with minimal required scope, and avoid passing tokens on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivanpruss/skills/vercel-deployment-watchdog)
- [Vercel account tokens](https://vercel.com/account/tokens)
- [curl](https://curl.se/)
- [jq](https://stedolan.github.io/jq/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; monitoring scripts emit human-readable text or JSON status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq, and uses VERCEL_TOKEN when Vercel API checks are enabled.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
