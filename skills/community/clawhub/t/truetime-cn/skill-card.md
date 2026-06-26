## Description: <br>
中文优先的精确时间处理：当前时间、相对/绝对偏移、跨时区、夏令时、农历干支、中国法定节假日（含调休补班）、24 节气。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sereinnyaa](https://clawhub.ai/user/sereinnyaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and users working in Chinese-language time-sensitive workflows use this skill to get precise current time, offsets, timezone conversions, Chinese holidays, lunar calendar details, and solar terms before making scheduling or deadline decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses broad activation guidance for many time-related phrases, which can increase automatic local tool calls. <br>
Mitigation: Use the skill when precise time, timezone, holiday, lunar calendar, or deadline calculations are relevant; narrow activation wording if fewer automatic calls are preferred. <br>
Risk: Chinese holiday data is bundled for 2026 and may be unavailable for later years. <br>
Mitigation: When the script reports missing holiday-year data, disclose that it is falling back to weekend-only handling and update the bundled holiday data when official schedules are published. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sereinnyaa/truetime-cn) <br>
- [cnLunar](https://github.com/OPN48/cnLunar) <br>
- [OpenClaw truetime reference](https://github.com/openclaw/skills/tree/main/skills/cccat6/truetime) <br>
- [2026 China public holiday notice](http://politics.people.com.cn/n1/2025/1104/c1001-40596715.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the bundled Python script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local time-calculation results; no network, credential, persistence, or destructive behavior was found in security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
