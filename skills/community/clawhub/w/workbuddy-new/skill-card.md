## Description:

Generates and applies custom WorkBuddy skins from a prompt or reference image by producing theme CSS, preview assets, and reversible local patch commands for WorkBuddy's installed app package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chugenice](https://clawhub.ai/user/chugenice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and WorkBuddy users use this skill to create, preview, apply, and restore personalized WorkBuddy interface skins. It is intended for local customization workflows where the user accepts the risk of modifying the installed WorkBuddy package.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies WorkBuddy's installed app.asar, which can invalidate signatures or disrupt updates until restored.

Mitigation: Use only on a personal WorkBuddy installation, confirm the target app.asar path before applying, and keep the generated app.asar.bak available for restore.

Risk: The apply flow uses a scheduled PowerShell restart path with weak integrity and cleanup controls.

Mitigation: Inspect the generated restart task and temporary script before execution, run from a trusted skill package only, and remove leftover temporary files or tasks after applying.

Risk: Untrusted theme packages or reference files could cause unsafe local file changes or unexpected UI behavior.

Mitigation: Use trusted local theme packages and reference files, avoid external resources, and preview generated skins before applying them to WorkBuddy.

## Reference(s):

- [WorkBuddy skin variable reference](artifact/references/variable-reference.md)
- [ClawHub skill page](https://clawhub.ai/chugenice/skills/workbuddy-new)
- [Publisher profile](https://clawhub.ai/user/chugenice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with PowerShell and Node.js command examples, plus generated CSS, HTML preview files, and theme configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local theme files and commands that modify WorkBuddy's installed app.asar after creating a backup.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
