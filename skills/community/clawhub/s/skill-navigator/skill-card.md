## Description: <br>
Provides a highly visual and interactive dashboard for OpenClaw users to easily understand and recall the functionalities of installed skills, featuring a visual overview, capability map, and contextual prompting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brandon-zhanghaodong](https://clawhub.ai/user/brandon-zhanghaodong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to scan installed skill metadata, summarize available capabilities, and generate a Markdown dashboard with a visual overview, capability map, and contextual skill suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local scanner reads SKILL.md metadata for every installed skill and prints that inventory. <br>
Mitigation: Avoid storing secrets in skill frontmatter and review the generated inventory before sharing it. <br>
Risk: The dashboard and contextual skill matches are generated from heuristic metadata parsing. <br>
Mitigation: Review dashboard content and treat skill suggestions as user-confirmed recommendations rather than automatic activation decisions. <br>


## Reference(s): <br>
- [API Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/brandon-zhanghaodong/skill-navigator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON skill inventory and Markdown dashboard template guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled scanner reads local SKILL.md frontmatter from installed skills and prints the resulting inventory as JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
