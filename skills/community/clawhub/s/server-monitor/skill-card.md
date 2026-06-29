## Description: <br>
Server Monitor is a markdown guide for basic Linux server health checks, SSH failure review, connection inspection, and load monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingaiwork](https://clawhub.ai/user/kingaiwork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and server operators use this skill to ask an agent for lightweight Linux monitoring guidance, including service status checks, failed SSH login review, connection summaries, and basic load inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides an agent to inspect local server status, SSH failure logs, and network connections. <br>
Mitigation: Review proposed commands before execution and run them only on systems where the user is authorized to inspect services, logs, and network state. <br>
Risk: The release evidence describes the skill as a lightweight guide rather than a complete automated monitoring system. <br>
Mitigation: Treat the output as operational guidance and command examples, not as a substitute for a deployed monitoring and alerting platform. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingaiwork/skills/server-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/kingaiwork) <br>
- [King AI Works homepage](https://kingai.work/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No installer or executable code; relies on standard Linux utilities listed in release evidence.] <br>

## Skill Version(s): <br>
2.0.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
