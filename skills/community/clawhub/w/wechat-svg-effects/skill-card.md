## Description:

Create interactive SVG/CSS effects for WeChat Official Account articles using pure SVG animations and inline CSS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content creators use this skill to generate WeChat-compatible interactive article effects such as click-to-reveal layers, animated SVG elements, 3D card effects, and inline CSS layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated WeChat article markup could include incorrect content, broken interactions, or unsuitable included media.

Mitigation: Review and test generated markup in the WeChat editor before publishing, including any images or article content requested from the agent.

Risk: Markup that uses JavaScript, style blocks, or external CSS will not match the skill's WeChat compatibility constraints.

Mitigation: Validate outputs before use to confirm there are no script tags, style blocks, or external CSS references.

## Reference(s):

- [Architecture Patterns & Animation Templates](references/patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown with XML, SVG, and inline CSS snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for WeChat Official Account article markup and should avoid JavaScript, style blocks, and external CSS.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
