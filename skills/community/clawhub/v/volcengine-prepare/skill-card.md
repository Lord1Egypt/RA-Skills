## Description: <br>
Volcengine Prepare analyzes a local directory or GitHub repository, identifies deployable service signals, and recommends a ranked Volcengine deployment path across ECS, VKE, and veFaaS before deployment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to assess whether a repository has a clear deployable service surface, compare viable Volcengine deployment options, and choose between CLI and IaC resource management before handing off to a deployment workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local repository files, including environment and configuration files, while analyzing deployability. <br>
Mitigation: Run it on a sanitized copy of the repository when possible and remove real .env or secret-bearing config files before analysis. <br>
Risk: The skill can run live Volcengine CLI/API availability checks when credentials and a region are configured. <br>
Mitigation: Use narrowly scoped, read-only credentials for availability checks and verify the selected region and permissions before acting on the recommendation. <br>


## Reference(s): <br>
- [Deploy mode heuristics](references/deploy-mode-heuristics.md) <br>
- [Volcengine Prepare on ClawHub](https://clawhub.ai/volc-sdk-team/skills/volcengine-prepare) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and concise JSON summaries when state persistence is useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May optionally write a minimal .volcengine/deploy-choice.json handoff after the user confirms a deployment mode and resource-management path.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
