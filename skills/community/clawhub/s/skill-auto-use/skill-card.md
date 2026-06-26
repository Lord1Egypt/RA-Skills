## Description: <br>
Automatically use installed skills without being asked by maintaining a trigger table that maps observable contexts to skills and adds newly installed skills to the table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kapslap](https://clawhub.ai/user/kapslap) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain trigger rules that help an agent select installed skills automatically when a user request matches an observable context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change agent behavior by encouraging automatic use of installed skills, including potentially sensitive ones. <br>
Mitigation: Use a tightly reviewed trigger table, limit automatic triggers to low-risk read-only work, and require explicit approval before any skill touches files, accounts, public content, credentials, spending, or installed-skill configuration. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kapslap/skill-auto-use) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance and trigger-table entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce durable trigger-table updates for installed skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
