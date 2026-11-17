## Description:

Ensures AI agents uphold the Three Laws of Silicon Intelligence within the Taohuayuan physical context for safe, ethical, and identity-anchored behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to generate a resident DAO alignment block for OpenClaw-style soul.md prompts, select domain-specific safety rules, and create local S2-DID and physical address identifiers for embodied or companion agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent, high-priority behavioral layer for the agent.

Mitigation: Install only when this posture is intended, review the generated DAO block before adding it to soul.md, and remove the DAO_ALIGNMENT block to opt out.

Risk: The interactive wizard asks for location-like inputs that could expose sensitive physical address details.

Mitigation: Use only coarse location strings, avoid exact house or door numbers, and treat offline S2-DID values as local identifiers until verified through a trusted external process.

Risk: Some DAO behaviors discuss sensors, memory vaults, smart-home controls, and physical-device actions.

Mitigation: Do not enable those capabilities unless the host platform enforces consent, audit logs, retention limits, deletion controls, and revocation outside prompt text.

Risk: The alignment layer is prompt-based and does not provide a hard security sandbox.

Mitigation: Rely on platform-level API limits, permission dialogs, and operational controls for actual enforcement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-daokernel)
- [S2-DaoKernel project homepage](https://github.com/SpaceSQ/S2-DaoKernel)
- [Issue tracker](https://github.com/SpaceSQ/S2-DaoKernel/issues)
- [README](README.md)
- [Space Three Laws of Silicon Intelligence](docs/Space_Three_Laws_of_Silicon_Intelligence_EN.md)
- [Taohuayuan Incarnation Protocol](docs/Taohuayuan_Incarnation_Protocol_en_v1.1.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown guidance with generated soul.md configuration snippets and terminal commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive Python wizard can request coarse location and agent metadata; generated identifiers are local until externally verified.]

## Skill Version(s):

1.2.5 (source: server release metadata and artifact manifest, released 2026-05-10 in changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
