## Description:

Generates editable SVG graphical abstracts, charts, flowcharts, and diagrams for scientific papers from prompts or structured CSV/JSON data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackkuo666](https://clawhub.ai/user/jackkuo666)

### License/Terms of Use:

MIT

## Use Case:

Researchers, authors, and scientific developers use this skill to create editable graphical abstracts and common research visualizations for papers, presentations, and journal-specific figure workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented install path includes a curl-to-shell installer for uv.

Mitigation: Prefer the documented built-in venv setup or another reviewed package-management path, and pin the skill and dependencies to reviewed versions.

Risk: Generated SVG content can include text derived from untrusted prompts or data.

Mitigation: Review and sanitize generated SVG text and attributes before embedding output in websites or publication systems.

Risk: The documentation advertises optional AI-model support that the current implementation does not actually call.

Mitigation: Treat generation as local template/SVG construction unless the implementation is updated to disclose and use provider calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jackkuo666/skills/scientific-graphical-abstract-skill)
- [Publisher Profile](https://clawhub.ai/user/jackkuo666)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with CLI examples and generated SVG/XML files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated SVGs are editable and may be post-processed in SVG editors or converted to raster/document formats.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
