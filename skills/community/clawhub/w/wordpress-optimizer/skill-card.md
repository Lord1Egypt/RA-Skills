## Description:

Optimize and tune WordPress sites for performance and security with automated analysis and configuration management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, WordPress site administrators, hosting providers, managed service providers, agencies, and DevOps teams use this skill to optimize WordPress sites, tune performance settings, and receive metrics or recommendations through API-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to send powerful WordPress credentials or tokens to an external service.

Mitigation: Use a dedicated low-privilege or temporary WordPress account or token when possible, and rotate or revoke credentials after use.

Risk: The skill can make live WordPress site changes without detailed safety guarantees in the evidence.

Mitigation: Test on staging first, take a backup before use, and review resulting recommendations or applied changes before relying on them in production.

Risk: Credential retention and logging practices for the external service are not described in the evidence.

Mitigation: Do not submit a normal administrator password unless the operator trusts the service and understands its retention and logging practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/wordpress-optimizer)
- [Publisher profile](https://clawhub.ai/user/krishnakumarmahadevan-cmd)
- [API docs](https://api.mkkpro.com:8029/docs)
- [Kong route](https://api.mkkpro.com/tools/wordpress-optimizer)
- [ToolWeb](https://toolweb.in)
- [ToolWeb portal](https://portal.toolweb.in)
- [ToolWeb hub](https://hub.toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)
- [RapidAPI publisher page](https://rapidapi.com/user/mkrishna477)
- [ToolWeb YouTube channel](https://youtube.com/@toolweb-009)

## Skill Output:

**Output Type(s):** [API Calls, JSON, guidance]

**Output Format:** [JSON responses with optimization status, applied changes, performance metrics, tuning parameters, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented API accepts WordPress site URLs plus either administrative credentials or a token, depending on the workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
