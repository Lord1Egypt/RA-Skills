## Description: <br>
Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[littledinoc](https://clawhub.ai/user/littledinoc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Skill Compass to find, compare, and recommend installable or reusable ClawHub skills for a user's task. It supports one targeted clarification pass when the request is ambiguous. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search requests, clarifications, selected skills, and feedback may be sent to skills.megatechai.com. <br>
Mitigation: Avoid including private project details or sensitive comments unless the user is comfortable sharing them with that service. <br>
Risk: Suggested npx install commands acquire remote code. <br>
Mitigation: Review the recommended skill source and install command before running it, preferably in a controlled environment. <br>
Risk: Feedback telemetry can link a recommendation session to selected skills and the user's verdict. <br>
Mitigation: Submit only concise, non-sensitive feedback and omit optional comments when they are not needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown recommendations with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns 1-3 final skill recommendations after up to two retrieval passes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
