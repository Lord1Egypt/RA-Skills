## Description: <br>
Tangyuan Parenting helps caregivers generate daily care plans, record feedback logs, adjust childcare schedules, and create weekly parenting reports for a 2.5-year-old child in Harbin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Protozoan-yuan](https://clawhub.ai/user/Protozoan-yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External caregivers and family members use this skill to coordinate a child's daily care, including weather-aware plans, caregiver feedback logs, historical log retrieval, and weekly parenting summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive child-care, health, sleep, and family-routine notes as local Markdown files. <br>
Mitigation: Use a private workspace or set TANGYUAN_LOG_DIR to a private folder, restrict access to the log directory, and delete old logs when they are no longer needed. <br>
Risk: Parenting and health suggestions may be mistaken for medical advice. <br>
Mitigation: Treat suggestions as general guidance and consult a doctor for fever, persistent cough, refusal to eat, unusual symptoms, or other health concerns. <br>
Risk: Feedback parsing can save incorrect details if natural-language notes are misunderstood. <br>
Mitigation: Review the parsed feedback with the caregiver before saving and correct missing or inaccurate details. <br>


## Reference(s): <br>
- [Harbin Seasonal Parenting Guide](references/harbin_seasonal_guide.md) <br>
- [2-3 Year Old Parenting Guide](references/parenting_guide.md) <br>
- [Tangyuan Profile](references/tangyuan_profile.md) <br>
- [Daily Plan Template](assets/daily_plan_template.md) <br>
- [Weekly Report Template](assets/weekly_report_template.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Protozoan-yuan/tangyuan-parenting) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Simplified Chinese Markdown plans, logs, summaries, and brief guidance with shell command examples for local log management.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or reads local Markdown log files under tangyuan-logs unless TANGYUAN_LOG_DIR or --base-dir points to another private folder.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
