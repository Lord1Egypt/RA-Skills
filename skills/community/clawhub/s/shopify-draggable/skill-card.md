## Description: <br>
Helps agents implement browser drag-and-drop interactions with @shopify/draggable, including basic dragging, sorting, drop zones, swapping, plugins, sensors, events, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to add drag-and-drop behavior to web interfaces such as sortable lists, kanban boards, draggable grids, and drop zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production apps could inherit dependency or compatibility risk from an older community-maintained drag-and-drop library. <br>
Mitigation: Pin the @shopify/draggable package version, review the library's maintenance and browser support status, and test drag behavior across target devices before release. <br>
Risk: Runtime CDN imports can introduce availability and supply-chain exposure in production web apps. <br>
Mitigation: Use CDN imports only for prototypes; prefer npm-installed, bundled builds for production deployments. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/openlark/shopify-draggable) <br>
- [jsDelivr @shopify/draggable ESM build](https://cdn.jsdelivr.net/npm/@shopify/draggable/build/esm/index.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript, HTML, CSS, and shell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no tool execution or credentials required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
