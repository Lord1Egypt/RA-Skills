## Description: <br>
计算时间区间内有多少个工作日的技能。支持排除中国的节假日和调休安排。当用户询问工作日计算、节假日排除、工作时间计算时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hunterxysy](https://clawhub.ai/user/hunterxysy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to calculate workdays between dates, excluding weekends and China holiday or adjusted-workday schedules. It can return simple counts, detailed day classifications, and JSON exports for downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional installer modifies local OpenClaw skill directories. <br>
Mitigation: Review the installer before running it and confirm the target installation directory is appropriate. <br>
Risk: The calculator can write JSON exports to a user-provided path. <br>
Mitigation: Choose export paths deliberately and avoid overwriting important files. <br>
Risk: Holiday data is embedded for 2025-2026 and may become stale. <br>
Mitigation: Update holiday data before relying on calculations outside the documented date coverage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hunterxysy/workday-calculator) <br>
- [Publisher profile](https://clawhub.ai/user/hunterxysy) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, code, guidance] <br>
**Output Format:** [Plain text command output, JSON export files, and Markdown guidance with bash and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calculations are local and use embedded China holiday and adjusted-workday data for 2025-2026.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
