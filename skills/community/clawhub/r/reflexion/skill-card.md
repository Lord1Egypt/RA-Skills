## Description: <br>
Closed-loop learning for AI coding agents that captures errors and corrections, recalls relevant past solutions, and promotes recurring patterns to project memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharoonsharif](https://clawhub.ai/user/sharoonsharif) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to capture command failures, user corrections, and recurring fixes, then recall or promote them as project memory for future coding tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic local capture and recall can store command output, user corrections, and project-specific context where local memory is not appropriate. <br>
Mitigation: Install only in projects where automatic local memory is acceptable, prefer project-level hooks, add .reflexion/ to .gitignore for private work, and narrow or disable hooks around sensitive output. <br>
Risk: Recalled or promoted learnings can become stale, overbroad, or misleading if they are not reviewed. <br>
Mitigation: Review captured entries and promoted rules periodically, and verify a recalled solution before treating it as current project guidance. <br>


## Reference(s): <br>
- [Integration Guide](references/integration.md) <br>
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) <br>
- [ClawHub reflexion release](https://clawhub.ai/sharoonsharif/reflexion) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local .reflexion JSON entries, keyword indexes, and promoted project-memory rules when hooks are installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
