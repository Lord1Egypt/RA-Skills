## Description: <br>
SAI Creator AI transforms SENKU-approved OJS/PKP article briefs into publishable HTML articles, fixed seven-slide social carousels, optional social captions, and a handoff JSON for re-validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nijam727](https://clawhub.ai/user/nijam727) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, journal teams, and publication operators use this skill to turn validated OJS/PKP intelligence briefs into accessible public article pages, SVG carousel assets, optional platform captions, and structured handoff data for downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Brief content can be placed directly into publishable HTML or SVG. <br>
Mitigation: Use trusted SENKU briefs, review generated markup before publication, and add escaping or sanitization before hosting outputs. <br>
Risk: The artifact advertises carousel template files that are not present in the package. <br>
Mitigation: Verify or supply trusted carousel templates before relying on carousel generation. <br>
Risk: Generated assets include a fixed commercial CTA target. <br>
Mitigation: Confirm that the openjournaltheme.com CTA is acceptable for the publication context before release. <br>
Risk: Packaging utilities can include files from a selected directory. <br>
Mitigation: Run packaging only on reviewed skill directories that do not contain unrelated private files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nijam727/sai-creator) <br>
- [Article Template Spec](references/article-template-spec.md) <br>
- [Carousel Spec](references/carousel-spec.md) <br>
- [CTA Variants](references/cta-variants.md) <br>
- [Open Journal Theme CTA target](https://openjournaltheme.com/) <br>
- [Schema.org Article](https://schema.org/Article) <br>
- [Schema Markup Validator](https://validator.schema.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML, SVG, JSON, text captions, and Markdown-style operational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are constrained to complete SENKU briefs and should pass validation for WCAG AA contrast, required alt text, schema.org Article metadata, CTA URL, file size, and source-grounded claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
