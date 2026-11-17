## Description:

Generate macOS/iOS Shortcuts by creating plist files. Use when asked to create shortcuts, automate workflows, build .shortcut files, or generate Shortcuts plists. Covers 1,155 actions (427 WF*Actions + 728 AppIntents), variable references, and control flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erik-agens](https://clawhub.ai/user/erik-agens)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to generate Apple Shortcuts workflows as plist-backed .shortcut files, including action arrays, variable references, control flow, and signing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated shortcuts can include actions that delete data, run scripts, send network requests, use AI services, read clipboard, device, or location data, or change system settings.

Mitigation: Inspect generated actions before signing or importing a shortcut, and require confirmation or preview steps when workflows affect personal data or system behavior.

Risk: Signing or importing a generated shortcut may make an unsafe or incorrect workflow easier to run from Apple's Shortcuts app.

Mitigation: Review the plist action list and parameters first, then sign and import only workflows that match the intended automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erik-agens/skills/shortcuts-skill)
- [Shortcut Plist Format](artifact/PLIST_FORMAT.md)
- [Shortcuts Actions Reference](artifact/ACTIONS.md)
- [AppIntents Reference](artifact/APPINTENTS.md)
- [Parameter Types Reference](artifact/PARAMETER_TYPES.md)
- [Variable Reference System](artifact/VARIABLES.md)
- [Control Flow Patterns](artifact/CONTROL_FLOW.md)
- [Content Item Filters Reference](artifact/FILTERS.md)
- [Complete Working Examples](artifact/EXAMPLES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with XML plist examples, .shortcut plist content, and shell commands for signing generated shortcuts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated shortcuts must be reviewed before signing or importing into Apple's Shortcuts app.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
