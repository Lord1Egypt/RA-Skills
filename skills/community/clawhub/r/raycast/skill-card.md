## Description: <br>
Build and maintain Raycast extensions using the Raycast API. Triggers on @raycast/api, List, Grid, Detail, Form, AI.ask, LocalStorage, Cache, showToast, and BrowserExtension. Use this repo's references/api/*.md files as the primary source of truth for component specs and API usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaif](https://clawhub.ai/user/xaif) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to build, fix, and maintain Raycast extensions with React, TypeScript, and @raycast/api components. It guides component selection, implementation patterns, feedback, persistence, restricted API access checks, and citation of the relevant local API reference. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Raycast extensions may read private clipboard text, browser tabs, selected files or text, OAuth tokens, or form passwords. <br>
Mitigation: Review generated extensions before use, add explicit user disclosure or confirmation before private content is sent to AI or external services, and avoid persistent storage for secrets unless a secure user-controlled mechanism is used. <br>
Risk: AI or external-service examples may move user-provided content outside the local extension context. <br>
Mitigation: Use environment access checks, handle failures visibly, and require user confirmation for sensitive content flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaif/raycast) <br>
- [Raycast Extensions Skill](artifact/SKILL.md) <br>
- [Raycast Extension Examples](artifact/examples.md) <br>
- [List Reference](artifact/references/api/list.md) <br>
- [Grid Reference](artifact/references/api/grid.md) <br>
- [Detail Reference](artifact/references/api/detail.md) <br>
- [Form Reference](artifact/references/api/form.md) <br>
- [Action Panel Reference](artifact/references/api/action-panel.md) <br>
- [Actions Reference](artifact/references/api/actions.md) <br>
- [AI Reference](artifact/references/api/ai.md) <br>
- [Browser Extension Reference](artifact/references/api/browser-extension.md) <br>
- [Clipboard Reference](artifact/references/api/clipboard.md) <br>
- [Environment Reference](artifact/references/api/environment.md) <br>
- [Caching Reference](artifact/references/api/caching.md) <br>
- [Storage Reference](artifact/references/api/storage.md) <br>
- [Toast Reference](artifact/references/api/toast.md) <br>
- [HUD Reference](artifact/references/api/hud.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with TypeScript and TSX code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May cite local Raycast API reference files used to produce the guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
