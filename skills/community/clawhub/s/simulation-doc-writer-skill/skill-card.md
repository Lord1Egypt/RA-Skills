## Description: <br>
Write, revise, or review Chinese documentation for communication simulation programs, including simulation manuals, model descriptions, experiment and reproduction guides, paper-to-code comparisons, and MATLAB file and function inventories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[orbisz](https://clawhub.ai/user/orbisz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and communication engineers use this skill to produce or review Chinese documentation for communication simulation code, especially MATLAB projects and paper-to-code reproduction work. It helps map algorithms, models, metrics, files, functions, parameters, outputs, and reproduction steps to concrete implementation evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact contains a self-evolution mechanism that asks the agent to write diary entries and propose changes to the skill after failed executions. <br>
Mitigation: Disable or ignore the self-evolution steps unless the user explicitly asks for persistent diary files or skill-change proposals. <br>
Risk: The artifact disagrees about whether generated documentation should use .txt or .md output. <br>
Mitigation: Confirm the desired output extension before creating files, and prefer the explicit user request when it conflicts with the artifact text. <br>
Risk: The skill can create documentation from code, papers, logs, and plots, so unsupported assumptions could become misleading technical guidance. <br>
Mitigation: Separate confirmed facts from assumptions, mark uncertain items as 待确认, and require source-backed mappings for algorithms, files, functions, parameters, and results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/orbisz/simulation-doc-writer-skill) <br>
- [Chinese communication simulation documentation template](references/communication-simulation-doc-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Chinese plain text or Markdown documentation with tables, checklists, runnable commands, and verification guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [For MATLAB projects, the intended output covers every .m file and every function; generated files may require a user-confirmed save location and output extension.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
