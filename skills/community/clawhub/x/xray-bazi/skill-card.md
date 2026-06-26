## Description: <br>
Bazi guides an agent through collecting birth details, calculating a Four Pillars chart, and producing a traditional Chinese astrology analysis using bundled reference tables and classical-text summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[x-rayluan](https://clawhub.ai/user/x-rayluan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill for guided Bazi charting, cultural interpretation, and entertainment-oriented fortune analysis. It collects personal birth information, validates calendar pillars when possible, and returns structured analysis, tables, and cautionary guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for names, former names, birth dates, birth time, sex, and birthplace, which can be identifying personal information. <br>
Mitigation: Ask for user consent before collecting birth details, collect only fields needed for the requested reading, and avoid retaining or reposting personal details outside the active task. <br>
Risk: The skill can call the apihz calendar API to verify date pillars, which may disclose a birth date to an external service. <br>
Mitigation: Request consent before making the API call, explain what date fields will be sent, and mark the chart as unverified if the user declines or the API is unavailable. <br>
Risk: The skill may use user-provided apihz API credentials. <br>
Mitigation: Do not ask users to paste personal API keys unless necessary, do not expose keys in shared outputs, and prefer the documented public low-frequency test credentials when appropriate. <br>
Risk: Astrology and fortune-telling outputs can be mistaken for factual, medical, financial, or life-decision advice. <br>
Mitigation: Frame results as cultural and entertainment-oriented interpretation, avoid extreme predictions, and direct users to qualified professionals for medical, financial, or legal decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/x-rayluan/xray-bazi) <br>
- [Publisher profile](https://clawhub.ai/user/x-rayluan) <br>
- [Five Elements and Heavenly Stems/Earthly Branches tables](artifact/references/wuxing-tables.md) <br>
- [Shichen time table](artifact/references/shichen-table.md) <br>
- [Dayun rules](artifact/references/dayun-rules.md) <br>
- [Classical Bazi text summaries](artifact/references/classical-texts.md) <br>
- [apihz specified-date calendar API endpoint](https://cn.apihz.cn/api/time/getzdday.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis with tables and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call an external calendar API for date-pillar verification; if verification is unavailable, the skill instructs the agent to mark affected pillars as needing review.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
