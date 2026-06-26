## Description: <br>
Agent vision for web pages - scene summaries, attention-ranked elements, annotated screenshots, and state diffing via SurfAgent's perception engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentossoftware](https://clawhub.ai/user/agentossoftware) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to understand live web pages, identify important interactive elements, request annotated screenshots, and verify page changes after browser actions through a local SurfAgent perception daemon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A local SurfAgent daemon and its bearer token can expose browser perception capabilities beyond the skill text itself. <br>
Mitigation: Install only when the local SurfAgent daemon is trusted, keep the daemon bound to localhost, and treat ~/.surfagent/daemon-token.txt as a secret. <br>
Risk: Using browser perception on sensitive pages can reveal passwords, account data, or private information to the agent workflow. <br>
Mitigation: Avoid using the skill on sensitive browser content unless the operator is comfortable with the agent seeing that content. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with tool names, parameter tables, example workflows, and daemon endpoint examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides agents to request scene summaries, ranked elements, annotated screenshots, state tokens, and scene diffs from SurfAgent tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
