## Description: <br>
Redline Annotate lets developers add a visual annotation overlay to generated HTML pages, collect element-level comments locally, and feed those comments back into Claude Code for edits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[times77](https://clawhub.ai/user/times77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers use this skill to review generated HTML in a browser, attach comments to specific page elements, and have Claude Code apply the requested changes to the source HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a persistent Claude prompt hook and runs a localhost server. <br>
Mitigation: Inspect ~/.claude/settings.json before use, stop or uninstall the server when finished, and install only in projects where that hook behavior is acceptable. <br>
Risk: Annotated page content is stored locally and injected into model context. <br>
Mitigation: Use the skill on non-sensitive HTML and review .redline-inbox.json before continuing with model-driven edits. <br>
Risk: The release has under-scoped local and browser execution paths. <br>
Mitigation: Prefer a revised version with a bundled selector helper, a fixed project inbox protected by an auth token, and cleanup handled by validated code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/times77/redline-annotate) <br>
- [@medv/finder selector helper](https://unpkg.com/@medv/finder@3.1.0/finder.js) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, generated annotated HTML, local JSON feedback, and source HTML edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates annotated HTML output, writes a local feedback inbox, and can configure a Claude Code UserPromptSubmit hook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
