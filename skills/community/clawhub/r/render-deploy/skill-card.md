## Description: <br>
Deploy applications on Render with codebase analysis, render.yaml Blueprint generation, MCP direct provisioning, and post-deploy verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to deploy applications to Render, choose between Blueprint and direct creation flows, validate prerequisites, and verify deployments after release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create cloud services, push deployment configuration, and operate Render deployments. <br>
Mitigation: Confirm the repository, branch, Render workspace, service plan, region, git commits or pushes, and environment variables before approving actions. <br>
Risk: Deployment secrets or useful infrastructure context could be exposed through chat, logs, or local memory. <br>
Mitigation: Keep real secrets out of chat, logs, and local memory unless deliberately chosen, and review ~/render-deploy/ periodically. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ivangdavila/render-deploy) <br>
- [Skill homepage](https://clawic.com/skills/render-deploy) <br>
- [Setup](artifact/setup.md) <br>
- [Codebase analysis](artifact/codebase-analysis.md) <br>
- [Blueprint workflow](artifact/blueprint-workflow.md) <br>
- [Direct creation](artifact/direct-creation.md) <br>
- [Troubleshooting](artifact/troubleshooting.md) <br>
- [Render Dashboard](https://dashboard.render.com) <br>
- [Render MCP endpoint](https://mcp.render.com) <br>
- [Render API endpoint](https://api.render.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include render.yaml configuration, prerequisite checks, deployment commands, and verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
