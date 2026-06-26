## Description: <br>
Manage Turso SQLite databases via CLI, including databases, groups, tokens, and replicas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Melvynx](https://clawhub.ai/user/Melvynx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to manage Turso and libSQL resources from an agent-assisted CLI workflow, including databases, groups, organizations, tokens, replicas, and plan commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Database, group, organization, and replica commands can change or delete Turso resources. <br>
Mitigation: Confirm the exact target resource, organization, and intended action before allowing destructive or topology-changing commands. <br>
Risk: Plan upgrade commands can affect billing or account entitlements. <br>
Mitigation: Require explicit user approval and organization context before running billing-related commands. <br>
Risk: Database tokens, especially non-expiring tokens, can expose long-lived access. <br>
Mitigation: Prefer expiring tokens, avoid placing tokens in logs, chat, or source files, and rotate credentials after use. <br>
Risk: The Linux setup path uses a curl-to-bash installer. <br>
Mitigation: Verify the installer source before execution and prefer a package-manager installation path when available. <br>


## Reference(s): <br>
- [ClawHub Turso Skill Release](https://clawhub.ai/Melvynx/turso) <br>
- [Melvynx Publisher Profile](https://clawhub.ai/user/Melvynx) <br>
- [Turso Linux Installer](https://get.tur.so/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and command tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance should prefer --output json where supported.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
