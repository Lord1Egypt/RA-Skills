## Description:

Turns natural language requests into scheduled voice notifications and structured briefings, with configuration guidance and examples for runtime-provided voice systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunxq1017-hash](https://clawhub.ai/user/sunxq1017-hash)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create or update scheduled spoken reminders, daily briefings, and other voice notification configurations. It helps structure timing, modules, language, voice, tone, and runtime handoff requirements without bundling a scheduler, TTS provider, or data connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may assume the package provides a complete scheduler, TTS engine, calendar connector, weather connector, or playback runtime.

Mitigation: Review runtime integrations separately and provide explicit adapters, credentials, and data sources outside the skill package.

Risk: Generated briefings can be incomplete or generic when optional weather, calendar, or other external inputs are unavailable.

Mitigation: Configure graceful fallback behavior and verify that required data is supplied by the user or runtime environment before relying on a spoken briefing.

## Reference(s):

- [Config Schema](references/config-schema.md)
- [Briefing Templates](references/briefing-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/sunxq1017-hash/skills/scheduled-voice-briefing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON configuration examples, and Python command-line examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are bounded to configured briefing modules and depend on runtime-provided voice, playback, and external data integrations.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
