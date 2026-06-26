## Description: <br>
AI-driven code review skill that examines code snippets, diffs, and pull request changes across security, performance, maintainability, logic, and style, then returns structured review findings with risk levels and repair suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caingao](https://clawhub.ai/user/caingao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review code before merge or release, with modes for full code review, PR review, focused security review, and quick pre-commit checks. It is intended to identify concrete issues, prioritize them by severity, and provide actionable fix examples. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect local git changes during PR review workflows, which may expose private or secret-bearing code to the reviewing agent. <br>
Mitigation: Invoke it with an explicit pasted snippet, a specific diff, or clearly named files, and confirm the repository scope before using it in private workspaces. <br>
Risk: Generated review findings and repair snippets may be incomplete or incorrect. <br>
Mitigation: Have a qualified developer verify findings and proposed patches before applying them or approving a merge. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/caingao/smart-code-review) <br>
- [Publisher Profile](https://clawhub.ai/user/caingao) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review reports with tables, severity sections, and inline code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can be tailored by review mode, strictness, target language, focus dimension, and response language.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and openclaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
