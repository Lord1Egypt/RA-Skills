## Description: <br>
根据教案、教材或课件生成交互式教学HTML网页. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erich1566](https://clawhub.ai/user/erich1566) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Educators, instructional designers, and developers use this skill to convert lesson material into interactive standalone HTML teaching pages with formulas, animations, and subject-specific presentation options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated teaching pages can load browser libraries from jsDelivr. <br>
Mitigation: Use the skill only where outbound CDN loading is acceptable, or bundle local vetted copies of the required libraries for offline or high-assurance classroom use. <br>
Risk: Lesson source text is inserted into generated HTML. <br>
Mitigation: Use trusted lesson files and add HTML escaping before publishing generated pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erich1566/teach-gen) <br>
- [Publisher profile](https://clawhub.ai/user/erich1566) <br>


## Skill Output: <br>
**Output Type(s):** [files, code, configuration] <br>
**Output Format:** [Standalone HTML file generated from lesson source content and CLI options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated pages may load browser libraries from jsDelivr unless the user bundles local vetted copies.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
