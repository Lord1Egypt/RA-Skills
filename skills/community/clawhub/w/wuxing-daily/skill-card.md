## Description: <br>
Wuxing Daily helps an agent provide Chinese traditional wuxing and Bazi analysis, daily fortune guidance, lunar date conversion, and optional reminder setup from a user's birth details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent for entertainment-oriented wuxing, Bazi, lunar calendar, and daily fortune readings based on birth date and optional birth hour. Developers can also use the bundled local Python scripts to calculate wuxing distributions, daily fortune text, and lunar date conversions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest fortune, wellness, finance, or decision-related guidance that users may over-weight. <br>
Mitigation: Present readings as cultural entertainment and avoid treating them as medical, financial, legal, or other professional advice. <br>
Risk: The optional daily reminder uses a cron-style scheduled command. <br>
Mitigation: Enable reminders only after reviewing the exact command and confirming how to list, modify, and remove the scheduled task. <br>
Risk: The artifact includes local Python scripts that run on the user's machine. <br>
Mitigation: Review the scripts before execution and run them in an appropriate local environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/timyljob2011-sudo/wuxing-daily) <br>
- [Nayin table reference](artifact/nayin_table.md) <br>
- [Wuxing daily-life reference](artifact/wuxing_daily.md) <br>
- [Ziwei star reference](artifact/ziwei_stars.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with optional Python and cron command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are cultural entertainment guidance and local script results; no hidden data access or network behavior was identified in server security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
