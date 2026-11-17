## Description: <br>
Ui Ux Dev Paid helps agents generate multi-page React UI projects, preserve design-system settings, review screenshots across device sizes, optimize images, and package static outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, design teams, and agencies use this skill to create multi-page React interfaces, manage project design settings, run screenshot review workflows, optimize image assets, and export deployable static packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent to create or modify local project files. <br>
Mitigation: Run it in a controlled workspace and review generated or changed files before use. <br>
Risk: The skill can direct an agent to run shell tools and browser-based screenshot workflows. <br>
Mitigation: Inspect proposed commands before execution and use a sandboxed local server or disposable project environment. <br>
Risk: Generated pages may load React, Tailwind, fonts, or other assets from public CDNs. <br>
Mitigation: Verify CDN usage against project policy and pin or self-host assets where required. <br>
Risk: Zip exports can include unintended files if project contents are not reviewed. <br>
Mitigation: Inspect archive contents before sharing or deploying generated packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ui-ux-dev-paid) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Tailwind CSS CDN](https://cdn.tailwindcss.com) <br>
- [React 18 UMD build](https://unpkg.com/react@18/umd/react.production.min.js) <br>
- [Google Fonts Inter](https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON, HTML, React, and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local project files, screenshots, WebP assets, optimization reports, and zip archives when the agent executes the described workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
