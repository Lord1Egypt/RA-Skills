## Description:

Generates Taobao product listing draft JSON and an Excel final-review sheet from manually prepared product materials, with publication left to human review and manual action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guowaa223](https://clawhub.ai/user/guowaa223)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers or ecommerce operators use this skill to prepare Taobao listing drafts and review sheets from local, manually edited product data. Outputs must be reviewed before publication because the release security evidence warns that compliance pass marks are unverified templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated drafts and audit sheets may mark listings as compliant without performing the promised compliance, material consistency, prohibited-word, pricing, inventory, or category checks.

Mitigation: Treat all generated files as unverified templates and complete manual review before any Taobao publication.

Risk: Local file-scope issues require care when selecting product identifiers and working directories.

Mitigation: Use controlled product ID formats and run the skill in a dedicated working directory containing only intended product inputs.

Risk: Runtime dependencies are specified as minimum versions rather than locked versions.

Mitigation: Pin or lock dependencies before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guowaa223/skills/taobao-draft-generator)
- [ClawHub publisher profile](https://clawhub.ai/user/guowaa223)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance and command examples; generated artifacts are JSON draft files and Excel review sheets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 with requests, pandas, openpyxl, and python-dotenv; ClawHub metadata lists Windows support.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
