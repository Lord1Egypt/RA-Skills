## Description: <br>
A Chinese-language QA requirement analysis skill that decomposes vague requirements into testable input, operation, state, output, and rule dimensions while surfacing explicit, implicit, and derived requirements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kokxi](https://clawhub.ai/user/kokxi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
QA engineers, product reviewers, and developers use this skill to break down PRDs, requirement text, URLs, or uploaded requirement documents into structured requirement IDs, business rules, five-dimension analysis, risks, and open questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate on broad requirement-analysis prompts. <br>
Mitigation: Use it intentionally for requirement decomposition tasks and review its output before feeding it into downstream QA or risk-analysis workflows. <br>
Risk: The skill may default to Chinese-language output. <br>
Mitigation: Ask the agent for the desired output language when a non-Chinese review artifact is needed. <br>
Risk: Requirement files or URLs supplied to the agent may contain sensitive product or business information. <br>
Mitigation: Provide only requirement content and links that are appropriate for the agent to read in the target environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kokxi/skills/qa-req-deconstruction) <br>
- [Publisher Profile](https://clawhub.ai/user/kokxi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown tables and lists, usually in Chinese] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include requirement IDs, explicit and implicit requirements, derived requirements, business rules, five-dimension decomposition, risk points, and questions.] <br>

## Skill Version(s): <br>
1.5.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
