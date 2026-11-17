## Description: <br>
A free UI/UX prototyping skill for individual developers that generates zero-build React pages from natural language, supports project preferences, screenshot-based visual review, WebP conversion, and static HTML export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and designers use this skill to quickly create single-page landing pages, portfolios, and event pages as CDN-based React prototypes, then review screenshots and refine the UI across desktop and mobile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and modify local project files while generating prototypes. <br>
Mitigation: Review proposed file paths and generated content before allowing writes outside the intended project directory. <br>
Risk: Preview, screenshot, and image-conversion workflows may require local Bash commands or package installation. <br>
Mitigation: Inspect commands before execution and avoid elevated privileges unless the user explicitly approves the dependency installation. <br>
Risk: Generated pages load React, Babel, and Tailwind from third-party CDNs. <br>
Mitigation: Confirm CDN use is acceptable for the project or replace CDN dependencies with approved local assets before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ui-ux-dev-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [React 18 UMD build](https://unpkg.com/react@18/umd/react.production.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JSON, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local static React HTML pages, project JSON configuration, screenshot review guidance, and WebP conversion commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
