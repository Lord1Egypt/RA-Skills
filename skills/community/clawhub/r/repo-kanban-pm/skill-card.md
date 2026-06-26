## Description: <br>
Installs a lightweight repository product-management workflow with roadmap status tracking, per-feature KANBAN boards, branch and PR conventions, bug intake, and an optional daily OpenClaw PM review cron. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Michailbul](https://clawhub.ai/user/Michailbul) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent teams use this skill to add a simple PM workflow to a new or existing code repository so feature work, bugs, branches, and PRs stay aligned. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Initialization writes PM documentation and may append workflow rules to AGENTS.md in the target repository. <br>
Mitigation: Run the init script from a clean branch or clean git state and review the generated files and AGENTS.md changes before committing. <br>
Risk: The optional daily cron can perform recurring automated PM reviews and may use local gh credentials or run repository checks. <br>
Mitigation: Enable the cron only when recurring review is intended, and choose the agent, schedule, timezone, and repository path deliberately. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated repository documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update repository PM files and AGENTS.md, and may configure an optional recurring OpenClaw cron review.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
