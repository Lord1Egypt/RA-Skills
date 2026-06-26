## Description: <br>
Creates and manages SubAgents for focused development, research, writing, data analysis, or custom tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aning35](https://clawhub.ai/user/aning35) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to design, launch, and manage focused SubAgents with preset roles for coding, research, writing, and data analysis. It helps choose run or session mode, define labels and task prompts, and provide management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SubAgents may be given tasks that are broader than necessary. <br>
Mitigation: Give each SubAgent a narrow task and use one-time run mode unless persistence is required. <br>
Risk: Persistent SubAgent sessions can continue beyond the immediate task. <br>
Mitigation: Review SubAgent logs and terminate sessions that are no longer needed. <br>
Risk: A separately obtained create-subagent.ps1 script may not match this reviewed package. <br>
Mitigation: Do not run external scripts unless they are separately reviewed and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aning35/reate-subagent) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown text with command and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes suggested SubAgent task prompts, labels, run/session mode selection, and management commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
