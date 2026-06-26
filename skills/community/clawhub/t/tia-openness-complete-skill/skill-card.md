## Description: <br>
基于TIA Openness API的完整PLC自动化技能，支持项目创建、硬件配置、SCL编程、编译下载 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiansiting](https://clawhub.ai/user/jiansiting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and industrial automation engineers use this skill to automate Siemens TIA Portal PLC engineering tasks, including project creation, S7-1200/1500 hardware setup, SCL block generation, compilation, and controller download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can compile and download PLC changes without built-in safety gates or confirmations. <br>
Mitigation: Run it only in a controlled engineering or lab environment unless additional safety controls are added, and verify project contents, backups, maintenance window, and operator approval before download or full_automation. <br>
Risk: Download actions can target the wrong controller or network interface if sample or incorrect values are used. <br>
Mitigation: Confirm the PLC identity, IP address, PG/PC interface, and target environment before execution; do not reuse bundled sample IP or password values as production configuration. <br>
Risk: Unpinned dependencies may change execution behavior over time. <br>
Mitigation: Pin and review dependencies before installation in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiansiting/tia-openness-complete-skill) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Files, Configuration, Guidance] <br>
**Output Format:** [JSON results, generated SCL code, TIA Portal project changes, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Actions return success status, messages, and operation-specific fields; workflows may create, compile, save, close, or download PLC project changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
