## Description: <br>
A traditional Chinese five-elements and Bazi astrology skill for calculating Wuxing attributes, interpreting birth-chart traits, generating daily fortune guidance, converting lunar dates, and optionally setting daily reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timyljob2011-sudo](https://clawhub.ai/user/timyljob2011-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users interested in Chinese traditional almanac and astrology use this skill to calculate Bazi and Wuxing profiles from birth information, convert lunar dates, and receive daily fortune or reminder guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional daily reminder can create a recurring local cron task. <br>
Mitigation: Only create the reminder after confirming the actual script path, the exact command being scheduled, and how to remove the task later. <br>
Risk: Fortune, diet, body, wellness, and major-decision suggestions may be mistaken for professional advice. <br>
Mitigation: Treat outputs as cultural entertainment and do not rely on them for medical, financial, legal, safety, or major life decisions. <br>
Risk: The documentation references scripts under a scripts/ directory while the release artifact places script files at the root. <br>
Mitigation: Verify file locations before running commands or scheduling reminders. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/timyljob2011-sudo/wuxingbazi-daily) <br>
- [Nayin Table](artifact/nayin_table.md) <br>
- [Wuxing Daily Correspondence](artifact/wuxing_daily.md) <br>
- [Ziwei Stars](artifact/ziwei_stars.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-style prose with command examples and plain-text fortune reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Bazi/Wuxing analysis, lunar-date conversion results, daily fortune ratings, auspicious/inauspicious suggestions, lucky elements, and optional cron reminder commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact docs list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
