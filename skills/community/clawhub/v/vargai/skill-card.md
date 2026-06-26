## Description: <br>
Generate AI videos, images, speech, and music using varg for videos, animations, talking characters, slideshows, product showcases, social content, and single-asset generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[securityqq](https://clawhub.ai/user/securityqq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to generate media assets and compose rendered videos through Varg cloud APIs or local Bun/ffmpeg workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source templates, media inputs, generated outputs, and API keys may be sent to Varg or provider services. <br>
Mitigation: Install only when Varg and the selected providers are trusted for the intended data, and avoid uploading sensitive or non-consensual personal media. <br>
Risk: API keys may be exposed through local files or copied commands. <br>
Mitigation: Keep .env files out of source control and review curl, bun, and BYOK commands before running them. <br>
Risk: Full renders can consume paid credits. <br>
Mitigation: Use local preview mode or cheaper models while iterating, and verify model pricing and duration constraints before paid renders. <br>
Risk: Returned S3 or output URLs may be shareable. <br>
Mitigation: Treat generated output links as potentially accessible unless Varg documentation confirms stronger access controls. <br>


## Reference(s): <br>
- [Varg homepage](https://varg.ai) <br>
- [ClawHub skill page](https://clawhub.ai/securityqq/vargai) <br>
- [Cloud Render Mode](references/cloud-render.md) <br>
- [Local Render Mode](references/local-render.md) <br>
- [Gateway API Reference](references/gateway-api.md) <br>
- [Model Catalog](references/models.md) <br>
- [Component Reference](references/components.md) <br>
- [Recipes & Patterns](references/recipes.md) <br>
- [Complete Templates](references/templates.md) <br>
- [Common Errors & Debugging](references/common-errors.md) <br>
- [Prompt Engineering Guide](references/prompting.md) <br>
- [Bring Your Own Key](references/byok.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript, TSX, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce curl requests, local render commands, Varg configuration guidance, and media-generation templates.] <br>

## Skill Version(s): <br>
2.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
