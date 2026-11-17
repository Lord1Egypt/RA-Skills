## Description:

Helps developers build and port VSD Craft and StreamDock plugins, including SDK communication, property inspectors, key and knob input, reconnection, testing, and packaging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create or port VSD Craft and StreamDock plugins, compare Elgato SDK behavior, test plugins with a mock host, and package releases. Real-device installation and hardware checks are separate, user-approved steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated plugins may have unreviewed behavior when installed in a real VSD Craft environment.

Mitigation: Review generated plugin contents before installation; obtain separate approval for changes to existing scenes or hardware.

Risk: Mock-host test results may be mistaken for real application or device validation.

Mitigation: Report mock-host, real-application, and physical-hardware results separately.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/nextaltair/skills/vsd-craft-plugin-development)
- [Elgato compatibility matrix](references/elgato-compatibility.md)
- [Development and verification guide](references/development.md)
- [Field observations](references/field-observations.md)
- [Compatibility research sources](references/sources.md)
- [StreamDock plugin SDK](https://sdk.key123.vip/en/guide/get-started.html)
- [Elgato Stream Deck plugin WebSocket reference](https://docs.elgato.com/streamdeck/sdk/references/websocket/plugin/)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and shell commands; generated plugin files and optional ZIP archive]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled tests use a mock host; real application and hardware behavior require separate checks.]

## Skill Version(s):

1.0.0 (source: ClawHub server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
