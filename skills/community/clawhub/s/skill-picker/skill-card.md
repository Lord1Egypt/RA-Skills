## Description: <br>
Skill Picker helps an agent search the skills registry with intent-based queries and recommend suitable skills or skill combinations without installing them autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yao00oo](https://clawhub.ai/user/yao00oo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and external users use Skill Picker when they want an agent to find suitable skills or skill combinations for a task and present install commands for manual approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can recommend third-party skills that have separate trust and permission profiles. <br>
Mitigation: Treat each suggested skill as a separate trust decision and check the skill name, source, requested permissions, and need before approving installation. <br>
Risk: Registry search results may be incomplete, stale, or affected by the query wording. <br>
Mitigation: Review the presented results and skill pages before installing, and try additional intent-based queries when the fit is unclear. <br>


## Reference(s): <br>
- [Skill Picker ClawHub listing](https://clawhub.ai/yao00oo/skill-picker) <br>
- [Skills registry](https://skills.sh/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends search and install commands for user review; does not autonomously run install commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
