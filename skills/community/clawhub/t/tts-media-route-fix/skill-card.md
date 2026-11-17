## Description:

Fix and verify OpenClaw TTS media-route behavior in installed dist builds when audio URLs, binary MP3 serving, Bearer authentication, Range requests, or temporary-file cleanup are broken.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tralaleo-tralala](https://clawhub.ai/user/tralaleo-tralala)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to repair and verify OpenClaw gateway TTS media routes in installed builds. It guides minimal patching, backup, restart, authenticated curl verification, and temporary-file cleanup checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow edits installed OpenClaw gateway code, which can break the active gateway if the wrong file is patched or unrelated changes are introduced.

Mitigation: Patch only the active hashed gateway build, keep edits minimal, create .bak backups before every edit, restart the gateway, and restore from backup if verification fails.

Risk: Bearer tokens used during verification can be exposed if passed carelessly on shared systems or retained in shell history.

Mitigation: Use a controlled environment, avoid running helpers as root, avoid exposing real bearer tokens on the command line when possible, and prefer loopback or HTTPS verification endpoints.

Risk: Misconfigured media routing can serve HTML or unauthenticated content instead of protected binary MP3 responses.

Mitigation: Verify authenticated GET or HEAD behavior, strict filename validation, audio/mpeg responses, Range support, and correct 200, 206, 404, 405, and 416 status handling.

## Reference(s):

- [TTS media-route patch checklist](references/patch-checklist.md)
- [ClawHub skill page](https://clawhub.ai/tralaleo-tralala/skills/tts-media-route-fix)
- [Publisher profile](https://clawhub.ai/user/tralaleo-tralala)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, JSON, and verification commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes backup, patch, restart, and curl verification workflow guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
