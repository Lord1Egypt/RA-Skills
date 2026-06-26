## Description: <br>
Dynamically creates and manages AI agent teams for complex tasks. Invoke when user requests multi-agent collaboration, complex project execution, or when tasks require specialized roles and coordinated workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ChenXinBest](https://clawhub.ai/user/ChenXinBest) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate multiple configured AI models for complex projects that benefit from task decomposition, role assignment, progress reporting, and review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider credentials may be persisted in local configuration. <br>
Mitigation: Use environment-variable references or a secret manager instead of raw API keys, keep `.trae/config` out of version control, and inspect generated configuration files before use. <br>
Risk: Full task content may be shared with multiple configured AI providers or models. <br>
Mitigation: Configure only providers that are approved to receive the task content and avoid routing sensitive work through unapproved models. <br>


## Reference(s): <br>
- [ClawHub TeamWork Skill](https://clawhub.ai/ChenXinBest/teamwork) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown, code, shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, generated report templates, and command-oriented setup steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create or update local provider, role, score, and report files under the agent workspace configuration paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
