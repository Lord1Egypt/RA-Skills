## Description: <br>
Web PPTX Generator helps agents create polished, mobile-friendly single-file HTML presentations using predefined themes, layout recipes, and local Node.js scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and business users use this skill to turn outlines, long-form notes, or structured content into polished HTML slide decks for pitches, reports, product launches, and technical presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated or previewed HTML can execute locally in a browser context. <br>
Mitigation: Keep generated files in a project folder and preview only trusted or skill-generated HTML. <br>
Risk: Preview rendering can depend on the local Chrome binary selected by the environment. <br>
Mitigation: Verify any CHROME_BIN override before rendering previews. <br>
Risk: The optional global preview renderer adds an extra local dependency. <br>
Mitigation: Install the optional global preview package only when preview image generation is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobewin/web-pptx-generator) <br>
- [Runtime](artifact/references/runtime.md) <br>
- [Assembly Workflow](artifact/references/assembly-workflow.md) <br>
- [Content Schema](artifact/references/content-schema.md) <br>
- [Theme Catalog](artifact/references/theme-catalog.md) <br>
- [Layout System](artifact/references/layout-system.md) <br>
- [Quality Bar](artifact/references/quality-bar.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, structured JSON content, shell commands, and single-file HTML presentation code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are designed for local Node.js workflows and may include optional preview-rendering commands.] <br>

## Skill Version(s): <br>
2.0.5 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
