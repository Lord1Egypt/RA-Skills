## Description:

Deploy applications on Render with codebase analysis, render.yaml Blueprint generation, MCP direct provisioning, and post-deploy verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and deployment engineers use this skill to assess an application, choose an appropriate Render deployment path, generate or apply deployment configuration, and verify the resulting service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide service creation, environment variable updates, git commits, pushes, and deployments.

Mitigation: Keep activation limited to explicit Render deployment requests and review each deployment-affecting action before execution.

Risk: Deployment metadata, repository URLs, environment variable names, and explicitly provided values may be sent to Render services.

Mitigation: Use the skill only when Render is the intended deployment target and confirm which configuration values should be sent.

Risk: Optional local memory can store deployment preferences, notes, environment inventories, and incident history.

Mitigation: Create or update local memory only after explicit user consent and avoid storing secret values unless the user specifically requests it.

## Reference(s):

- [Render Deploy on ClawHub](https://clawhub.ai/ivangdavila/skills/render-deploy)
- [Render Dashboard](https://dashboard.render.com)
- [Render MCP](https://mcp.render.com)
- [Render API](https://api.render.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, YAML, JSON, and plain-text command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Render Blueprint configuration, direct provisioning steps, prerequisite checks, and deployment verification guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
