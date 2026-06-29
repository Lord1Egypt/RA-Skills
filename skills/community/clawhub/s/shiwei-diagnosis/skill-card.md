## Description: <br>
施炜诊断方法论 helps an agent structure Chinese enterprise management diagnosis from company materials, interviews, and survey evidence into diagnostic Markdown and presentation-ready guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tuobadaidai](https://clawhub.ai/user/tuobadaidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External consultants, business leaders, and strategy teams use this skill to run structured management-consulting diagnosis, assess organizational capabilities, identify growth-stage constraints, and draft change recommendations. It is most appropriate when the user can provide company materials, interview notes, and survey data for triangulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled scripts include unsafe local command execution. <br>
Mitigation: Run scripts only in a controlled workspace and review commands before execution. <br>
Risk: The PPT generator contains client-specific content and a hard-coded output path. <br>
Mitigation: Revise generate_ppt.js to remove client-specific material and require an explicit output path before use. <br>
Risk: Management diagnosis can involve confidential interview, HR, financial, and leadership materials. <br>
Mitigation: Use redacted inputs unless the publisher and execution environment are trusted. <br>


## Reference(s): <br>
- [Diagnosis Framework](references/diagnosis-framework.md) <br>
- [Markdown Diagnosis Template](references/md-template.md) <br>
- [PPT Structure and Audit Checklist](references/ppt-structure.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/tuobadaidai/skills/shiwei-diagnosis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional JavaScript and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce structured diagnosis Markdown and guide PPT generation and audit workflows.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
