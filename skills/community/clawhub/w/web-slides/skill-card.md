## Description: <br>
Professional single-page HTML presentation generator for creating polished web-based slide decks with multiple themes, mobile-friendly output, and optional PDF export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and presentation authors use this skill to turn outlines or structured content into polished single-file HTML slide decks for pitches, reports, product launches, technical talks, and business presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs local Node-based generation tools and may use an external npm dependency. <br>
Mitigation: Review and pin external npm dependencies before global installation. <br>
Risk: Preview rendering can execute arbitrary generated or user-provided HTML in a browser context. <br>
Mitigation: Keep CHROME_BIN pointed at a trusted browser and avoid preview-rendering untrusted HTML. <br>


## Reference(s): <br>
- [Web Slides Skill Page](https://clawhub.ai/tobewin/web-slides) <br>
- [Runtime](references/runtime.md) <br>
- [Theme Catalog](references/theme-catalog.md) <br>
- [Layout System](references/layout-system.md) <br>
- [Content Schema](references/content-schema.md) <br>
- [Assembly Workflow](references/assembly-workflow.md) <br>
- [Quality Bar](references/quality-bar.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, JSON deck content, and single-file HTML presentation code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Node-based generation and validation scripts; optional preview rendering depends on a trusted Chrome binary.] <br>

## Skill Version(s): <br>
2.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
