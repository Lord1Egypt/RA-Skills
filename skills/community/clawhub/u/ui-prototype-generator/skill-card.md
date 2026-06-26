## Description: <br>
Creates interactive UI prototypes from reference images or descriptions, generating HTML by default and optional Figma designs only when explicitly requested. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhappy](https://clawhub.ai/user/zhappy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to turn screenshots or product descriptions into browser-previewable UI prototypes, reusable component structures, and optional Figma handoff artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Figma output uses a Figma access token and may send screenshots or internal design details to Figma. <br>
Mitigation: Configure a Figma token only when Figma output is needed, keep the token out of Git and shared logs, and use confidential design inputs only when project policy allows it. <br>
Risk: Generated prototypes may misread a reference image or encode UI behavior that has not been reviewed. <br>
Mitigation: Review generated HTML or Figma artifacts, test interactions, and adjust implementation details before relying on the prototype for product or design decisions. <br>


## Reference(s): <br>
- [HTML Components](references/HTML_COMPONENTS.md) <br>
- [Figma Components](references/FIGMA_COMPONENTS.md) <br>
- [Design Tokens](references/DESIGN_TOKENS.md) <br>
- [Examples](references/EXAMPLES.md) <br>
- [Figma API Documentation](https://www.figma.com/developers/api) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with generated HTML files, optional Figma file URLs, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [HTML is the default output; Figma output requires explicit user request and a Figma access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, CHANGELOG, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
