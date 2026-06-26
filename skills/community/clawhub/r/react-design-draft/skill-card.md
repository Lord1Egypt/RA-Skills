## Description: <br>
Generate React design drafts (4-piece set) from content. Invoke for 'design draft'/'设计稿'/'生成页面'/'信息图'/'知识卡片'/'多图配图'. Do NOT use for editing existing code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, content creators, and design-focused agent users use this skill to turn articles or structured content into editable React visual drafts, including single information graphics and multi-illustration sets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read a local brand profile or inspect referenced project style files, which may expose sensitive values if those files contain secrets. <br>
Mitigation: Use trusted project references only, inspect CSS and token files before pointing the skill at them, and remove secrets from style-related files. <br>
Risk: Generated React design drafts may be mistaken for production application code. <br>
Mitigation: Review generated files before reuse and treat them as editable visual drafts rather than production-ready application changes. <br>


## Reference(s): <br>
- [React Design Draft ClawHub Page](https://clawhub.ai/edwardwason/react-design-draft) <br>
- [README](README.md) <br>
- [Content Layout Mapping](references/content-layout-mapping.md) <br>
- [Aesthetics Guide](references/aesthetics-guide.md) <br>
- [Density Standards](references/density-standards.md) <br>
- [React Output Spec](references/react-output-spec.md) <br>
- [Style Presets](references/style-presets.md) <br>
- [Brand Profile System](references/brand-profile.md) <br>
- [Chart System](references/chart-system.md) <br>
- [Image Sources](references/image-sources.md) <br>
- [Multi-Illustration Mode](references/multi-illustration.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with React, CSS, JavaScript, and file-tree outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates editable React design draft assets such as design-tokens.css, data.js, components/*.jsx, App.jsx, and preview/edit guidance.] <br>

## Skill Version(s): <br>
5.3.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
