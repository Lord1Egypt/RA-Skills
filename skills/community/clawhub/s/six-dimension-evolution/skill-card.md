## Description: <br>
Six-dimension evolution system for AI agents. Transform from reactive assistant to proactive partner with lessons tracking, success patterns, decision review, preference tracking, skill statistics, and knowledge gap detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stephongao](https://clawhub.ai/user/stephongao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up recurring memory, review, preference, decision, success, lesson, and knowledge-gap files for an agent self-improvement workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sets up recurring memory reviews that read conversation history. <br>
Mitigation: Install only when an always-on agent memory and review system is intended, and regularly inspect or delete generated memory, preference, review, conflict, and log files. <br>
Risk: Generated reports can be sent externally when Feishu delivery is enabled or configured. <br>
Mitigation: Disable or explicitly configure Feishu delivery before activation and review the exact HEARTBEAT.md changes. <br>
Risk: Activation modifies workspace memory and heartbeat files. <br>
Mitigation: Back up existing memory files before activation and review proposed file changes before applying them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stephongao/six-dimension-evolution) <br>
- [Publisher profile](https://clawhub.ai/user/stephongao) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates workspace memory, review, preference, decision, lesson, success, knowledge-gap, heartbeat, and log files when activated.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
