## Description: <br>
Quality gates and auto-healing guidance for AI-assisted personal software development. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ai-acheng](https://clawhub.ai/user/ai-acheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to run a structured quality-gate checklist before delivering AI-assisted code, with extra review prompts for high-risk features, semantic test selectors, business-aligned assertions, explicit dependencies, and debuggable failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that the runtime can report success without actually checking the project. <br>
Mitigation: Treat results as advisory until the implementation is reviewed or completed; require independent tests or manual review before relying on a pass result. <br>
Risk: The skill gives broad automatic repair instructions that could change dependencies, generated files, or source code without enough user approval. <br>
Mitigation: Use version control, inspect diffs, and require explicit approval before dependency changes, generated files, or broad auto-fixes are applied. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ai-acheng/qcsd-quality-gates) <br>
- [Publisher profile](https://clawhub.ai/user/ai-acheng) <br>
- [Project homepage](https://github.com/DrPepper8888/qcsd-quality-gates) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, code review findings, configuration] <br>
**Output Format:** [Markdown guidance and structured check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May report checked status, fixed items, issue lists, and AI-generated-code checklist results.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
