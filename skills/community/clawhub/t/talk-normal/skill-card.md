## Description:

talk-normal installs a bilingual style prompt into AGENTS.md to reduce verbose, corporate-sounding agent responses while preserving useful information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexiecs](https://clawhub.ai/user/hexiecs)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use talk-normal to install an always-on style prompt that makes OpenClaw or compatible agents answer more directly in English and Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can persistently change agent instructions beyond the intended workspace if it resolves a broader AGENTS.md path.

Mitigation: Review prompt.md and the reported AGENTS.md path before installing; run from the intended workspace and uninstall with bash install.sh --uninstall when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexiecs/skills/talk-normal)
- [Publisher profile](https://clawhub.ai/user/hexiecs)
- [Project homepage](https://github.com/hexiecs/talk-normal)
- [Issue tracker](https://github.com/hexiecs/talk-normal/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and an AGENTS.md prompt block]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installer writes a marked block to AGENTS.md and can remove it with --uninstall.]

## Skill Version(s):

0.6.2 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
