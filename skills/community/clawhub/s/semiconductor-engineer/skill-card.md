## Description: <br>
AI半导体工程师 is a semiconductor engineering assistant for device physics calculations, process lookup, IC design and verification guidance, yield and failure analysis, materials data lookup, and EDA tool support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bettermen](https://clawhub.ai/user/bettermen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Semiconductor engineers, chip designers, process engineers, yield engineers, and equipment engineers use this skill to calculate device parameters, compare semiconductor materials and process nodes, diagnose yield or failure issues, draft design and verification guidance, and generate engineering reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EDA and IC-design workflow branches may use external search, which can expose proprietary engineering details if sensitive prompt content is included. <br>
Mitigation: Use the skill only with non-sensitive semiconductor research inputs unless external search disclosure is acceptable; do not include proprietary design files, process details, tool logs, customer data, or unreleased product information in prompts. <br>
Risk: The skill includes typical semiconductor formulas and reference parameters that may not match a specific fab, process design kit, or production qualification context. <br>
Mitigation: Treat calculations and tables as preliminary engineering guidance and verify results against authoritative process specifications, PDK documentation, and internal review before production decisions. <br>


## Reference(s): <br>
- [Semiconductor Physics Reference](artifact/references/semiconductor_physics.md) <br>
- [Process Technology Reference](artifact/references/process_technology.md) <br>
- [Materials Data Reference](artifact/references/materials_data.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, code blocks, shell commands, and optional single-file HTML reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include semiconductor calculation results, material comparison tables, diagnostic checklists, SPICE or RTL snippets, and report-generation guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
