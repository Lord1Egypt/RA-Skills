## Description: <br>
Use when choosing a DESIGN.md style, applying a style to a web project, generating page prompts or template recipes, browsing bundled source systems, or checking UI code against a selected visual style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuwei1125](https://clawhub.ai/user/liuwei1125) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use Vibe UI to select visual styles, apply DESIGN.md guidance, generate page-specific prompts or template recipes, and check web UI code for design consistency. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write DESIGN.md, DESIGN.generated.md, .vibe-ui metadata, reports, and generated prompt artifacts in the active project. <br>
Mitigation: Run it in the intended project workspace and review generated files before committing or using them in production. <br>
Risk: The extract-url command can fetch a URL or process HTML supplied by the user. <br>
Mitigation: Use extract-url only with public or trusted URLs, especially in corporate environments. <br>
Risk: Bundled style and template references are inspired by public UI patterns and may mention upstream systems. <br>
Mitigation: Avoid copying logos, trademarks, proprietary assets, screenshots, or official brand claims from inspiration sources. <br>
Risk: Static design checks are a first-pass review and may miss rendering, accessibility, or implementation defects. <br>
Mitigation: Inspect the rendered UI and run the project test suite in addition to Vibe UI reports. <br>


## Reference(s): <br>
- [Vibe UI README](artifact/README.md) <br>
- [Vibe UI Skill Definition](artifact/SKILL.md) <br>
- [Open Design Attribution](artifact/resource/open-design-attribution.md) <br>
- [Resource Sync Manifest](artifact/resource/resources-sync-manifest.json) <br>
- [Security Policy](artifact/SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance, shell commands, JSON metadata, DESIGN.md files, reports, and generated prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write DESIGN.md, DESIGN.generated.md, .vibe-ui JSON metadata, design reports, and local static browser output in the project where commands are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: changelog, package.json, and server release evidence; released 2026-06-04) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
