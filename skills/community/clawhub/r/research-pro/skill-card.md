## Description: <br>
科研专项工作流 - 参考 AutoResearchClaw 23阶段全流程，从想法到论文。覆盖文献调研、实验设计、代码实现、统计分析、论文写作。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers and developers use Research Pro to structure a Chinese-first research workflow from idea definition through literature review, experiment design, implementation planning, statistical analysis, peer review, and paper drafting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can lead an agent toward experiment execution, generated code, dataset use, helper-agent coordination, or other concrete actions. <br>
Mitigation: Review and approve the specific commands, files, datasets, invoked skills, and helper-agent actions before allowing execution. <br>
Risk: Research outputs can contain incorrect citations, unreproducible results, or unverified claims if generated without review. <br>
Mitigation: Use the skill's human-in-the-loop checkpoints, require real database-backed citations, verify claims, and reproduce experiment results before relying on generated research material. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured templates, tables, code blocks, and command prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first research workflow guidance with human-in-the-loop checkpoints and citation, reproducibility, and claim-verification expectations.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
