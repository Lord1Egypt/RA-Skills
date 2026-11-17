## Description:

DOM capture engine that can export any DOM subtree as SVG, PNG, JPG, WebP, Canvas, or Blob, supporting inline styles, fonts, background images, pseudo-elements, and Shadow DOM.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to install and apply SnapDOM when they need to capture selected web page elements, DOM nodes, or HTML fragments as image, Canvas, SVG, Blob, or data URL outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples load mutable third-party JavaScript from a public CDN.

Mitigation: Pin and locally bundle trusted SnapDOM dependencies before using the skill in sensitive or production workflows.

Risk: Examples show use of a public CORS proxy that may expose requested asset URLs or page context.

Mitigation: Avoid the public proxy unless it is fully trusted; use a controlled proxy or only CORS-accessible assets.

Risk: DOM capture on private or authenticated pages can include sensitive visible content.

Mitigation: Capture only explicitly selected elements and exclude or redact sensitive fields before export.

## Reference(s):

- [SnapDOM API Reference](artifact/references/api_reference.md)
- [SnapDOM Demo](artifact/assets/demo.html)
- [DOM Capture Engine on ClawHub](https://clawhub.ai/openlark/skills/snapdom)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with JavaScript, HTML, and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents toward browser-context execution and DOM capture outputs such as image elements, SVG, Canvas, Blob, or data URLs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
