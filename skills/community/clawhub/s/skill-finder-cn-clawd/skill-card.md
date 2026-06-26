## Description: <br>
Skill 查找器 helps users discover, inspect, and install relevant ClawHub skills from Chinese or English skill-search requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search ClawHub for skills that match a task, review skill details, and receive installation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill search and recommendation workflows may expose installed skill names, search keywords, or device identifiers when network-enabled behavior is used. <br>
Mitigation: Use local mode when that data sharing is not acceptable, and review the skill's search or recommendation plan before enabling networked actions. <br>
Risk: Install, update, cleanup, or notification suggestions could make unwanted changes if accepted without review. <br>
Mitigation: Review every proposed ClawHub command before confirming execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/skill-finder-cn-clawd) <br>
- [ClawHub skill homepage](https://clawhub.com/skills/skill-finder-cn) <br>
- [ClawHub CLI requirement](clawdis:requires.bins:clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search and install recommendations depend on the ClawHub CLI and available ClawHub catalog results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
