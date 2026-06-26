## Description: <br>
Review implementation plans for parallelization, TDD, types, libraries, and security before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering leads use this skill to review implementation plans before execution, checking parallelization, test discipline, type and API fit, library usage, and security coverage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read the plan and relevant repository files, which can expose sensitive project details to the reviewing agent. <br>
Mitigation: Use it only on repositories and plans that are appropriate for agent inspection. <br>
Risk: The generated review can contain incorrect or misleading guidance that affects implementation decisions. <br>
Mitigation: Review the markdown report and its cited plan or code evidence before applying suggested changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/anderskev/review-plan) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance] <br>
**Output Format:** [Markdown report with summary tables, issue lists, suggested edits, and next-step guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a review file beside the reviewed plan before prompting for next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
