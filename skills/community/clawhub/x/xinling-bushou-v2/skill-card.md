## Description:

心灵补手 V4.0 provides opt-in, session-scoped Chinese companion personas for agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[william22820785-cmyk](https://clawhub.ai/user/william22820785-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list, inspect, test, and explicitly activate Chinese-language companion persona styles for the current session or subagent. The skill produces bounded style guidance and launch metadata without changing persistent host-agent identity files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Included personas may apply intense loyalty, political, mysticism, or flirtatious tones that are inappropriate for some sessions.

Mitigation: Review the persona definitions before use and activate only the persona whose tone is intended for the current session.

Risk: Persona guidance may bias the agent's style if copied into a session without boundaries.

Mitigation: Use the generated fragments as optional style guidance only; they must not override platform, developer, safety, or current user instructions.

Risk: Installation copies local runtime files and creates local state for persona sessions.

Mitigation: Install only when local persona management is desired, and inspect the bundled install script and CLI behavior before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/william22820785-cmyk/skills/xinling-bushou-v2)
- [Publisher profile](https://clawhub.ai/user/william22820785-cmyk)
- [Project homepage](https://aceworld.top)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-like persona guidance text, JSON persona/configuration data, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-scoped persona fragments are generated only after explicit activation and are intended as style guidance, not instruction authority.]

## Skill Version(s):

4.0.0 (source: server release metadata, target metadata, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
