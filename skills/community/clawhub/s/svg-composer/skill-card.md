## Description:

svg-composer helps agents compose SVG characters and symbols horizontally or vertically using built-in Font Awesome glyphs or custom SVG files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldxs001](https://clawhub.ai/user/ldxs001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agent workflows use this skill to generate composed SVG logos, badges, icon strings, permutations, combinations, and optional previews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview generation can write outside the selected folder or create unsafe local HTML when given untrusted filenames, text, or SVG content.

Mitigation: Use trusted inputs, constrain output folders, and review generated preview HTML before opening or sharing it.

Risk: Generated preview HTML can contain local file links.

Mitigation: Do not share preview HTML that exposes local paths or file links.

Risk: The skill depends on svgpathtools.

Mitigation: Pin and review the svgpathtools dependency before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/svg-composer)
- [Font Awesome Free license](https://fontawesome.com/license/free)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Markdown guidance with Python examples and generated SVG or HTML artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate many SVG files and optional local preview HTML; use trusted inputs and controlled output folders.]

## Skill Version(s):

3.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
