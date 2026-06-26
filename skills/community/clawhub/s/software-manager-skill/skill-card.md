## Description: <br>
Software Manager Skill helps an agent run an active product-management workflow for requirements analysis, PRD writing, product planning, competitive analysis, data analysis, Mermaid diagrams, document export, and optional interactive H5 prototypes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yhongm](https://clawhub.ai/user/yhongm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers, founders, developers, and agents use this skill to turn product ideas or product questions into clarified requirements, product plans, PRDs, Mermaid diagrams, exportable documents, and optional browser-openable H5 prototypes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use product details in web searches during research. <br>
Mitigation: Avoid providing sensitive product, customer, or business-confidential details unless that disclosure is acceptable. <br>
Risk: Optional export and diagram features may require local Node.js, npm, Python packages, and browser-based rendering. <br>
Mitigation: Install optional dependencies only in trusted environments and review generated PRD, DOCX, diagram, and H5 outputs before sharing. <br>
Risk: Generated files are written to user-directed paths. <br>
Mitigation: Choose export paths deliberately and review requested paths before allowing file writes. <br>
Risk: The H5 prototype instructions include mixed claims about zero external dependencies versus Tailwind CDN use. <br>
Mitigation: Confirm whether offline-only output or CDN-backed output is required before generating or distributing prototypes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yhongm/software-manager-skill) <br>
- [Publisher profile](https://clawhub.ai/user/yhongm) <br>
- [README](README.md) <br>
- [PRD template](references/prd-template.md) <br>
- [PM framework](references/pm-framework.md) <br>
- [PM responsibilities](references/pm-responsibilities.md) <br>
- [SDLC product process](references/sdlc-product-process.md) <br>
- [Mermaid guide](references/mermaid-guide.md) <br>
- [Atlassian Agile](https://www.atlassian.com/software-development-lifecycle) <br>
- [Scrum Guide](https://www.scrumguides.org/) <br>
- [Mermaid Documentation](https://mermaid.js.org/) <br>
- [Tailwind CSS Chinese documentation](https://www.tailwindcss.cn/) <br>
- [Lucide](https://lucide.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Mermaid diagrams, HTML/CSS/JavaScript prototype code, and optional local document files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write user-directed Markdown, DOCX, PNG-rendered diagrams, or single-file HTML prototypes when requested.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
