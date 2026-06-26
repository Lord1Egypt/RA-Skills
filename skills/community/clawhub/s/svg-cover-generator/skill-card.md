## Description: <br>
Create polished, editable SVG cover artwork for reports, articles, slide decks, social cards, ebook covers, posters, and landing-page hero images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NimaChu](https://clawhub.ai/user/NimaChu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, designers, and content creators use this skill to generate self-contained, editable SVG covers for reports, slide decks, social cards, posters, ebook covers, and hero images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SVG files can overwrite existing files when the user asks the agent to save output to a path. <br>
Mitigation: Choose destination paths deliberately and avoid overwriting important files. <br>
Risk: SVG output may be structurally invalid or may include unintended external references if not checked. <br>
Mitigation: Run the bundled local SVG validator against saved SVG files before delivery. <br>


## Reference(s): <br>
- [SVG Cover Design Rules](references/design-rules.md) <br>
- [Layout Recipes](references/layout-recipes.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/NimaChu/svg-cover-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown with fenced SVG code blocks or saved SVG files plus concise validation notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended to be self-contained SVG with editable text, inline styles, no remote assets, and optional local validation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
