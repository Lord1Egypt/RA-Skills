## Description: <br>
Guarantee instruction compliance with root cause analysis, flow verification, and automated validators that make future failures impossible. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an instruction failure must not repeat. It guides root cause analysis, verifies whether future agents will see the corrected rule, and proposes local validators for enforceable prevention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local records under ~/self-discipline/. <br>
Mitigation: Review the directory contents and incident details before approving setup or ongoing use. <br>
Risk: Generated validator scripts can block messages, commits, or actions if integrated into an agent runtime or git hook. <br>
Mitigation: Review every generated validator script and run it in a dry-run mode before enabling enforcement. <br>
Risk: Suggested edits to AGENTS.md, HEARTBEAT.md, or similar files can change future agent behavior. <br>
Mitigation: Approve only exact proposed changes and keep a backup before modifying existing context files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/self-discipline) <br>
- [Skill homepage](https://clawic.com/skills/self-discipline) <br>
- [Setup guide](artifact/setup.md) <br>
- [Flow verification guide](artifact/flow-verification.md) <br>
- [Validator patterns](artifact/validators.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with optional shell script snippets and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local rule, incident, flow-analysis, and validator guidance for files under ~/self-discipline/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
