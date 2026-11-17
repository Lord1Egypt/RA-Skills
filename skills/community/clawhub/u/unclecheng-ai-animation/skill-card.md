## Description:

Transforms popular-science or technical explanatory content into single-page HTML presentation animations, with a default PPT-style carousel mode and an optional flowchart-style visual reconstruction mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unclecheng-li](https://clawhub.ai/user/unclecheng-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and technical content creators use this skill to turn explanatory text into HTML-based presentation or flowchart animations for teaching, video, and knowledge-sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated presentation HTML may contact mutable third-party CDNs when opened.

Mitigation: Remove or vendor remote scripts and fonts, pin dependency versions, and add integrity checks before distribution.

Risk: Generated HTML may contain leftover demo content or unsafe prompt examples.

Mitigation: Review the completed HTML before publishing, teaching, or using it in video production.

Risk: The workflow can write an HTML output file to a user-selected or default path.

Mitigation: Confirm the output destination before file writes and avoid overwriting existing work without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unclecheng-li/skills/unclecheng-ai-animation)
- [README](README.md)
- [PPT template selection guide](assets/templates/PPT Template-level2/SUMMARY.md)
- [Animation template selection guide](assets/templates/Animation/SUMMARY.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with generated HTML/CSS/JavaScript code or HTML file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses bundled HTML presentation and animation templates; generated pages may reference third-party CDN assets unless removed or vendored.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
