## Description: <br>
Query system information including OS, CPU, memory, and disk usage for basic configuration checks, resource usage review, and performance diagnostics across Windows, Linux, and macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liujintao-2021](https://clawhub.ai/user/liujintao-2021) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to inspect local operating system, CPU, memory, and disk details from an agent session. It is useful for lightweight environment checks and troubleshooting before or during local work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README installation command and skill metadata use different package names, which could lead users to install the wrong package. <br>
Mitigation: Confirm the package name before installing; the server-resolved release target is system-info-skill. <br>
Risk: Local OS, CPU, memory, and disk details may be printed into an agent session or logs. <br>
Mitigation: Use the skill only when sharing local system details in the current session and logs is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liujintao-2021/system-info-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands] <br>
**Output Format:** [Plain text table or JSON from a local Python script, with shell commands for invocation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter output to OS, CPU, memory, or disk details.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
