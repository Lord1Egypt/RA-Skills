## Description: <br>
Set up and run OpenAI Symphony with isolated issue workspaces, workflow contracts, and unattended Codex orchestration for Linear projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use this skill to set up trusted Linear-to-Codex orchestration with repository-owned workflow contracts, isolated issue workspaces, and operational runbooks for unattended coding runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill coordinates unattended Linear, Git, and Codex workflows with repository write access, so it can have high operational privilege in trusted projects. <br>
Mitigation: Install only for trusted Linear projects and repositories; confirm the repository, workspace root, tracker project, and terminal states before enabling unattended runs. <br>
Risk: Required API keys and Git credentials could expose tracker, model, or repository access if stored carelessly. <br>
Mitigation: Use least-privilege tokens and keep secrets out of ~/symphony/ memory files and workflow documentation. <br>
Risk: Workspace hooks and clone targets can run setup commands that affect local repositories or files. <br>
Mitigation: Review or pin clone targets and setup commands, keep hooks inside the issue workspace, and start rollout with approval_policy on-request or stricter. <br>


## Reference(s): <br>
- [OpenAI Symphony on ClawHub](https://clawhub.ai/ivangdavila/symphony) <br>
- [Skill homepage](https://clawic.com/skills/symphony) <br>
- [Upstream Symphony specification](https://github.com/openai/symphony/blob/main/SPEC.md) <br>
- [OpenAI Symphony repository](https://github.com/openai/symphony) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs focus on setup guidance, workflow contracts, safety checks, runbooks, and incident-response notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
