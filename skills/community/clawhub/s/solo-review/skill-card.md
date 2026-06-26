## Description: <br>
Review runs a final code review and quality gate by testing, checking coverage and security, verifying spec acceptance criteria, and producing a ship-ready report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill before shipping or after deployment to run a structured quality gate across tests, build health, security, acceptance criteria, documentation, logs, and code quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run local project commands and inspect deployment logs as part of the review workflow. <br>
Mitigation: Run it only in trusted repositories and review command output before relying on the verdict. <br>
Risk: The skill can edit review or planning documentation, create commits, and influence pipeline flow. <br>
Mitigation: Review diffs and commit contents before accepting changes, especially in repositories with automated deployment pipelines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/fortunto2/solo-review) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown review report with command results, file references, verdict, recommendations, and optional pipeline signal] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update review or planning documentation and create commits when the skill workflow calls for those actions.] <br>

## Skill Version(s): <br>
1.1.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
