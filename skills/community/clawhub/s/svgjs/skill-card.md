## Description:

SVG.js is a documentation-only skill for using the lightweight SVG manipulation and animation library, covering chainable APIs for creating, positioning, styling, animating, importing, and exporting SVG elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when generating or reviewing SVG.js code for vector graphics, data visualizations, SVG-based UI components, animation flows, and SVG DOM manipulation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated SVG.js guidance may import or transform SVG, HTML, or XML from untrusted sources if copied directly into an application.

Mitigation: Verify the npm package used by the project and sanitize or review untrusted SVG, HTML, and XML before importing it.

Risk: Examples may produce invisible or incorrect SVG output when required sizing, animation chaining, container geometry, text layout, or path structure constraints are missed.

Mitigation: Review generated code for explicit SVG size(), correct animate() sequencing, appropriate nested containers, explicit text line handling, and matching path command structures.

## Reference(s):

- [Shape Elements](references/shapes.md)
- [Text, Images, Masks, Gradients](references/text-image.md)
- [Manipulating Elements](references/manipulating.md)
- [Animating](references/animating.md)
- [Container Elements](references/containers.md)
- [Events](references/events.md)
- [Utilities](references/utilities.md)
- [Utility Classes](references/classes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Markdown responses with JavaScript and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no hidden runtime behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
