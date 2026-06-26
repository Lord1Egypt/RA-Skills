## Description: <br>
State Preservation & Identity Resurrection Infrastructure Tool (SPIRIT) preserves AI agent identity, memory, and projects to a private Git repository. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gopinathnelluri](https://clawhub.ai/user/gopinathnelluri) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to configure SPIRIT state synchronization, restore agent state on another machine, and optionally schedule recurring backups. It is intended for agent identity, memory, and project files that the user deliberately chooses to preserve in a private Git repository. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent identity, memory, and project files may contain sensitive information and can be uploaded repeatedly to Git. <br>
Mitigation: Use a dedicated private repository, inspect and narrow `.spirit-tracked`, and avoid including secrets or unrelated project data in synced files. <br>
Risk: The skill depends on an external SPIRIT installer or Homebrew tap. <br>
Mitigation: Verify the SPIRIT installer or Homebrew tap before installation and install only when SPIRIT state backup is intentional. <br>
Risk: Cron or auto-backup can create continuous background synchronization. <br>
Mitigation: Enable scheduled sync only when recurring backups are desired, and monitor the SPIRIT sync log and repository contents. <br>


## Reference(s): <br>
- [SPIRIT State Sync ClawHub listing](https://clawhub.ai/gopinathnelluri/spirit) <br>
- [SPIRIT project repository](https://github.com/TheOrionAI/spirit) <br>
- [SPIRIT installer](https://theorionai.github.io/spirit/install.sh) <br>
- [SPIRIT Cron Setup Guide](references/cron-setup.md) <br>
- [GitHub CLI](https://cli.github.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, sync, restore, authentication, and scheduling instructions for SPIRIT.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
