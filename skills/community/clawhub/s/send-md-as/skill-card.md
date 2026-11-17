## Description:

Render Markdown as polished media for messaging apps, with support for code highlighting, LaTeX, Mermaid diagrams, tables, themes, and optional page splitting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enc-hanted](https://clawhub.ai/user/enc-hanted)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to convert Markdown into JPEG, PNG, WebP, or PDF media and optionally send the rendered output through OpenClaw messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation uses user-level pip and npm packages, and the security summary flags unpinned dependency installation as review-worthy.

Mitigation: Install and run only where user-level dependency installation is acceptable, and pin or review dependencies before deployment.

Risk: The security summary flags unsafe temporary file handling, and the renderer writes temporary HTML under /tmp during rendering.

Mitigation: Avoid rendering secrets or private notes, verify the destination before sending media, and isolate the renderer until temporary-file handling is fixed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/enc-hanted/skills/send-md-as)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash commands; rendered media files as JPEG, PNG, WebP, or PDF]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports light, dark, sepia, and nord themes; image pagination is optional and should be requested explicitly.]

## Skill Version(s):

0.4.1 (source: server evidence, _meta.json, SKILL.md heading, render.sh VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
