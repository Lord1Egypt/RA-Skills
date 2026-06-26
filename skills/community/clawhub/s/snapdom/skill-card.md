## Description: <br>
DOM capture engine that can export any DOM subtree as SVG, PNG, JPG, WebP, Canvas, or Blob, supporting inline styles, fonts, background images, pseudo-elements, and Shadow DOM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to capture web page elements, DOM nodes, or HTML fragments and export them as image, canvas, blob, or SVG outputs. It is useful for browser automation workflows that need reusable DOM snapshots or one-off screenshots of selected elements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: DOM captures can include private page content if used on authenticated pages, tokenized URLs, internal dashboards, or elements the user did not intend to capture. <br>
Mitigation: Use the skill only on page elements intended for capture and review selectors before export. <br>
Risk: The optional third-party CORS proxy example may expose private or sensitive assets when used with internal or authenticated content. <br>
Mitigation: Use same-origin assets or a trusted self-hosted proxy instead of the example third-party proxy for private content. <br>
Risk: Unpinned npm or CDN dependencies can change between runs. <br>
Mitigation: Prefer pinned npm or CDN versions for repeatable execution. <br>


## Reference(s): <br>
- [SnapDOM API Reference](references/api_reference.md) <br>
- [Example Demo HTML](assets/demo.html) <br>
- [ClawHub skill page](https://clawhub.ai/openlark/snapdom) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with JavaScript, HTML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs guide an agent to produce DOM capture code, export-format choices, and integration instructions; captured images are produced by the user's browser/runtime, not by the skill card itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
