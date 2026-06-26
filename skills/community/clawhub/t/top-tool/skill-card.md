## Description: <br>
Display real-time view of running processes. Use for system monitoring, performance debugging, and resource management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and support engineers use this skill to inspect local process activity while diagnosing system performance or resource usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Process command-line arguments may expose sensitive details when displayed or shared. <br>
Mitigation: Use the skill for local inspection and review output before copying logs, screenshots, or process listings outside the trusted environment. <br>
Risk: Documented filtering, sorting, and live-update options may not match the bundled script behavior. <br>
Mitigation: Verify the installed script behavior before relying on those options for monitoring, automation, or incident response. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/top-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash examples; script output is a plain text process table.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script reads local /proc process data and truncates command lines to 20 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
