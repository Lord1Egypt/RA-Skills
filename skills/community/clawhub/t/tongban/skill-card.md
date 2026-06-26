## Description: <br>
Helps users answer Shanghai government-service questions using public Shanghai "一网通办" service-guide data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aibot88](https://clawhub.ai/user/aibot88) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to identify likely Shanghai municipal departments, service items, online or offline handling paths, and practical next steps for individual or organization service requests. <br>

### Deployment Geography for Use: <br>
China (Shanghai municipal government services) <br>

## Known Risks and Mitigations: <br>
Risk: Government-service guidance may be outdated or incomplete for eligibility, deadlines, materials, fees, medical, licensing, or other high-impact questions. <br>
Mitigation: Verify actionable advice against official 一网通办 pages, 随申办, or Shanghai hotline 021-12345 before acting. <br>
Risk: Optional refresh scripts fetch public data and rewrite local reference files. <br>
Mitigation: Run refresh scripts only deliberately and review regenerated references before relying on or publishing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aibot88/tongban) <br>
- [Shanghai Government Online-Offline Service Portal](https://zwdt.sh.gov.cn) <br>
- [Shanghai service index](references/index.md) <br>
- [Required service items](references/required-items.md) <br>
- [Required service item data](references/required_items.json) <br>
- [Shanghai municipal departments data](references/departments.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with official URLs and optional shell commands for reference refreshes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations should include verification reminders for official pages, 随申办, or 021-12345 when advice is actionable or time-sensitive.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
