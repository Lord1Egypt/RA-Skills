## Description: <br>
Create a PRD through user interview, codebase exploration, and module design, then submit as a GitHub issue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LiuHe12](https://clawhub.ai/user/LiuHe12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and product teams use this skill to interview stakeholders, inspect relevant repository context, define implementation and testing decisions, and draft a PRD for a planned feature. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository content more broadly than intended. <br>
Mitigation: Scope codebase exploration to specific files, directories, or modules before invoking the skill. <br>
Risk: The skill directs the agent to submit the PRD as a GitHub issue without an explicit final approval step. <br>
Mitigation: Require explicit approval of the target repository, issue title, and complete issue body before anything is posted. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown PRD suitable for a GitHub issue] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes problem statement, solution, user stories, implementation decisions, testing decisions, out-of-scope items, and further notes.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
