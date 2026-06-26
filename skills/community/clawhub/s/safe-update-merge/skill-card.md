## Description: <br>
Safely merges upstream OpenClaw updates into a fork while preserving custom plugin, UI, workspace, controller, and state extensions through a two-phase merge and user-confirmed promotion workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators maintaining customized OpenClaw forks use this skill to inspect upstream divergence, run dry-run or branch-based merges, preserve local customizations, validate builds, restart the gateway, and promote the result only after verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can merge code, build dependencies, restart the gateway, and force-push during promotion. <br>
Mitigation: Run dry-run first, use a disposable clone or isolated environment for review, and run promotion only after confirming the gateway is healthy. <br>
Risk: Conflict resolution can send redacted conflicted file content to Claude through the optional Claude CLI. <br>
Mitigation: Use manual conflict resolution with no auto-resolve when model transmission is not acceptable, and review redaction behavior before use. <br>
Risk: The bundled background sessions panel can read transcripts and send messages to cron or background sessions. <br>
Mitigation: Review or remove the background sessions panel before installation if transcript viewing or background-session messaging is outside the deployment's policy. <br>
Risk: Dependency install and build steps may pull packages or execute project build behavior in the target repository. <br>
Mitigation: Review upstream package changes from the preflight report and run the merge in an isolated environment before applying it to a live fork. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick-software/safe-update-merge) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Merge manifest](artifact/MERGE_MANIFEST.json) <br>
- [Safe merge update script](artifact/scripts/safe-merge-update.sh) <br>
- [Preflight script](artifact/scripts/preflight.sh) <br>
- [Validation script](artifact/scripts/validate.sh) <br>
- [Update modal reference](artifact/update-modal.ts) <br>
- [Background sessions backend reference](artifact/references/bg-sessions-backend.ts) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, code edits, configuration steps, and merge status reporting] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REPO_DIR and git; may use npm or pnpm, optional Claude CLI, optional systemctl, and fork-specific remote and branch settings.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
