## Description: <br>
Find, compare, and recommend agent skills across ClawHub and Skills.sh for capability gaps, workflow improvements, safer alternatives, and install decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to discover, compare, and select installable skills across ClawHub and Skills.sh when a task may benefit from a specialized agent capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flagged the skill as suspicious because setup can persistently change agent routing outside the local folder it claims to stay within. <br>
Mitigation: Keep setup limited to ~/skill-finder/ unless the user explicitly approves AGENTS.md or routing memory changes. <br>
Risk: Search and install workflows may involve external registry queries or skill installation decisions. <br>
Mitigation: Require confirmation before external searches or any skill installation, and review candidate skills before installing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/skill-finder) <br>
- [Skill homepage](https://clawic.com/skills/skill-finder) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with recommendations, comparisons, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local preference files under ~/skill-finder/ when the user explicitly chooses settings or asks to save preferences.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
