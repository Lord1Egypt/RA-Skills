## Description: <br>
Manage Vercel projects, deployments, domains, environment variables, and team resources via the Vercel REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect deployments, manage projects, configure domains, update environment variables, and automate Vercel DevOps workflows from an agent chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform high-impact Vercel write operations, including changes to deployments, domains, environment variables, secrets, and team membership. <br>
Mitigation: Review ClawLink previews and approve writes only when the proposed resource, scope, and production impact match the user's intent. <br>
Risk: The skill requires a connected Vercel account and handles sensitive credentials through ClawLink. <br>
Mitigation: Install only when the user accepts the ClawLink connection model, and verify the Vercel integration status before making tool calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/vercel-deployments) <br>
- [Vercel REST API Documentation](https://vercel.com/docs/rest-api) <br>
- [ClawLink Docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink Verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live ClawLink Vercel tool catalog as the source of truth before tool execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
