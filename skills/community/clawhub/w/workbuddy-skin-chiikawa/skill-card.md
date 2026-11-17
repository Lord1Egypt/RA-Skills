## Description:

Applies and customizes a WorkBuddy desktop skin with a Chiikawa-style animated background, glass UI styling, calendar highlighting, and sound-enabled interaction elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuzen-so](https://clawhub.ai/user/kuzen-so)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and customization-oriented developers use this skill to apply, pause, and adjust a runtime desktop skin for the WorkBuddy Electron app. It is useful for cosmetic customization workflows that should avoid modifying app.asar or permanent app resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The auto-install path can leave WorkBuddy launched with a persistent local debugging port and broad renderer debugging control.

Mitigation: Prefer the one-shot apply/pause workflow unless automatic reinjection is explicitly needed, and remove the startup flag when finished.

Risk: The LaunchAgent watcher can automatically reinject code when WorkBuddy starts.

Mitigation: Install the watcher only with user consent and verify that uninstall-auto.sh removes the LaunchAgent.

Risk: The startup flag installer changes the WorkBuddy executable launch path to add the debugging port.

Mitigation: Verify uninstall-flag.sh restores the original executable and rerun checks after WorkBuddy updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kuzen-so/skills/workbuddy-skin-chiikawa)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file-editing instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local Node.js and shell commands against a WorkBuddy installation when the user asks to apply or remove the skin.]

## Skill Version(s):

1.6.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
