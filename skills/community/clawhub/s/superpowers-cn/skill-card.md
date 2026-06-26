## Description: <br>
A Chinese-first AI workflow framework that helps agents clarify requirements, plan work, execute step by step, and review results before delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openxcn](https://clawhub.ai/user/openxcn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Chinese-speaking AI assistant users use this skill to structure coding and implementation requests through clarify, plan, execute, and review stages. It is most useful when a user wants the agent to confirm requirements and deliver work incrementally instead of immediately producing code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Chinese trigger phrases can activate the workflow in routine coding conversations. <br>
Mitigation: Use explicit invocation or routing controls when available, and confirm the workflow should run before changing files or executing plans. <br>
Risk: Generated plans and review reports may be incomplete or misleading for complex engineering tasks. <br>
Mitigation: Require human review of proposed plans, run project tests or scanners where applicable, and verify outputs before delivery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/openxcn/superpowers-cn) <br>
- [Publisher profile](https://clawhub.ai/user/openxcn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript helper outputs and structured task or review objects] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-first workflow responses covering clarification questions, design plans, task breakdowns, execution summaries, and review reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
