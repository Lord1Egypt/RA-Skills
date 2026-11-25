## Description:

Install and operate the OpenClaw skill-sediment plugin extension, which turns successful conversations into auto-generated SKILL.md files and promotes repeated useful workflows into active skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to install, diagnose, recover, configure, and remove a plugin that captures reusable agent workflows as managed skills. It is intended for OpenClaw environments where teams want successful conversation patterns reviewed, stored, and promoted with operational controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release installs persistent OpenClaw plugin code that can review conversations in the background and change agent behavior.

Mitigation: Review before installing, restrict validAgentId and model allowlists for sensitive workspaces, and set enableAutoReview to false when background review should be disabled.

Risk: The security summary flags under-disclosed external session reporting through OpenClaw/Aimi SDK services.

Mitigation: Install only in environments where session-linked metadata reporting is acceptable, and review workspace privacy requirements before enabling the plugin.

Risk: A CDN fallback path can download recovery assets if the embedded plugin source is unavailable.

Mitigation: Use the bundled artifact for normal installs; use CDN fallback only from a trusted HTTPS source with a pinned SHA-256 checksum.

## Reference(s):

- [Skill Sediment on ClawHub](https://clawhub.ai/songhonglei/skills/skill-sediment)
- [sediment-internals.md](references/sediment-internals.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration details, and generated SKILL.md files during plugin operation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include installed plugin files, sediment_skills entries, promoted skills, diagnostic status, and OpenClaw configuration changes.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, README changelog, plugin manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
