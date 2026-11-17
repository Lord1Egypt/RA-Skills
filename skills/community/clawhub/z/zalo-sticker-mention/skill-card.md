## Description:

Patches the @openclaw/zalouser channel driver to add outgoing group-chat auto-mentions and keyword-triggered Zalo sticker delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tuanminhhole](https://clawhub.ai/user/tuanminhhole)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw bot managers use this skill to patch @openclaw/zalouser so group chat replies can mention the latest sender and trigger a Zalo sticker with a trailing keyword marker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The patch script rewrites installed Zalo channel driver files across OpenClaw paths without enough scoping or confirmation.

Mitigation: Run it only in an isolated or test OpenClaw workspace, inspect the target files before applying changes, and keep the restore command available.

Risk: The publish helper is intended for maintainers and includes shell-command and unpinned-CLI risks.

Mitigation: Do not run scripts/publish.js unless maintaining the package and after reviewing and fixing those release-workflow risks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tuanminhhole/skills/zalo-sticker-mention)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and trailing sticker marker syntax]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent responses may include at most one trailing [Sticker: <keyword>] marker when contextually appropriate.]

## Skill Version(s):

1.0.2 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
