## Description: <br>
Install, search, update, and manage skills from public registries like ClawHub and SkillHub using the clawhub CLI within an OpenClaw or USM workspace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hulk-yin](https://clawhub.ai/user/hulk-yin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agent operators use this skill to find, install, update, and manage reusable skills from registries, then prepare them for use across OpenClaw or USM-managed agent workspaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages installation and updates for other skills, which can change future agent behavior across workspaces. <br>
Mitigation: Require explicit approval for each install, update, and CLI setup step, and review third-party skill contents before enabling them. <br>
Risk: Bulk update commands can modify multiple installed skills at once. <br>
Mitigation: Avoid `clawhub update --all` unless the expected changes have been reviewed; prefer updating a specific slug when possible. <br>
Risk: Workspace and symlink provisioning can distribute an unreviewed skill across multiple agent environments. <br>
Mitigation: Verify the target write locations, scope configuration, and symlink destinations before restarting agents or gateways. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hulk-yin/skill-installer-usm) <br>
- [ClawHub registry](https://clawhub.ai) <br>
- [skill-manager project](https://github.com/ZiweiAxis/skill-manager) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and installation, update, and workspace-configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the clawhub CLI to be available before install, search, or update commands can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
