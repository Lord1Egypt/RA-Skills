## Description: <br>
Generate macOS/iOS Shortcuts by creating plist files for import into Apple's Shortcuts app. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erik-agens](https://clawhub.ai/user/erik-agens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to generate plist-based macOS/iOS Shortcuts, including action arrays, variable references, control-flow blocks, and signing commands for import into Apple's Shortcuts app. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated shortcuts may include actions that delete content, run scripts, access sensitive data, make network requests, use AI actions, or change system settings. <br>
Mitigation: Inspect generated shortcuts before signing, importing, or running them, and add confirmation steps for destructive workflows. <br>
Risk: Shortcut actions that send text or context to AI or network services may expose sensitive information. <br>
Mitigation: Avoid sending sensitive text, personal data, or local context to AI or network actions unless the processing location and data handling are understood. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/erik-agens/shortcuts-skill) <br>
- [Shortcut Plist Format](artifact/PLIST_FORMAT.md) <br>
- [Shortcuts Actions Reference](artifact/ACTIONS.md) <br>
- [AppIntents Reference](artifact/APPINTENTS.md) <br>
- [Parameter Types Reference](artifact/PARAMETER_TYPES.md) <br>
- [Variable Reference System](artifact/VARIABLES.md) <br>
- [Control Flow Patterns](artifact/CONTROL_FLOW.md) <br>
- [Content Item Filters Reference](artifact/FILTERS.md) <br>
- [Complete Working Examples](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with XML plist examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces plist structures and signing guidance for .shortcut files; generated shortcuts should be inspected before import or execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
