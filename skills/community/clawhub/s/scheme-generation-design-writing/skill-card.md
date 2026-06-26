## Description: <br>
Generates UI/UX concept proposal templates and design specification documents from historical project materials and optional Figma design inputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shaco223](https://clawhub.ai/user/shaco223) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Designers, product teams, and implementation agents use this skill to match relevant historical projects, draft concept proposal content, and generate structured design descriptions for local image or Figma-based UI/UX work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup guidance discusses weakening Figma HTTPS verification while handling Figma tokens and design data. <br>
Mitigation: Use proper certificate or proxy configuration instead of disabling SSL/TLS verification; keep the Figma token read-only and protect any .env file. <br>
Risk: Generated project indexes and design documents may contain sensitive project or design information. <br>
Mitigation: Point the skill only at deliberately scoped project folders, use it only for materials you are authorized to process, and treat generated indexes and output documents as sensitive. <br>


## Reference(s): <br>
- [Concept plan schema](references/concept_plan_schema.md) <br>
- [Design description schema](references/design_desc_schema.md) <br>
- [Examples](references/examples.md) <br>
- [Quick start](references/quick-start.md) <br>
- [Figma](https://www.figma.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and generated document content intended for Word document output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local project indexes and configured output paths; Figma support depends on a separately configured Figma skill and token.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
