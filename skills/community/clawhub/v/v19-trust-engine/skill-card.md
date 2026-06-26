## Description: <br>
V19 Trust Engine explains a trust-scoring and VPAV validation model for agents, including weighted trust-score dimensions, certification thresholds, activity decay, and example calls to the V19 governance service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent developers use this documentation skill to understand how V19 calculates trust, validates declared capabilities against behavior, and gates certification status. It also provides example governance-service calls for health checks, trust-score lookup, and self-registration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes example calls to an external governance service. <br>
Mitigation: Verify the endpoint is trusted before running the curl examples. <br>
Risk: Self-registration can return a Pro key and may send agent details to the service. <br>
Mitigation: Avoid submitting sensitive agent details and keep any returned Pro key private. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/liuyanfeng1234/v19-trust-engine) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [V19 Governance Dashboard](https://boat-atlas-spa-flexible.trycloudflare.com/governance/dashboard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; example API calls may return governance-service responses when run by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
