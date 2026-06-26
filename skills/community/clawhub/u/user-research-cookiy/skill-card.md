## Description: <br>
Plans, runs, and synthesizes user research across qualitative interviews and quantitative surveys, including Cookiy AI workflows for recruitment, AI-moderated interviews, survey creation, billing, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenglin97](https://clawhub.ai/user/chenglin97) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, product teams, founders, and agents use this skill to design research plans, create interview guides or surveys, run Cookiy AI studies, recruit participants, and turn transcripts or survey results into research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can require Cookiy access tokens and may process participant or research data. <br>
Mitigation: Allow only the Cookiy API domain where possible, avoid pasting raw access tokens or unredacted participant data into chat, and use the skill only for intended research workflows. <br>
Risk: Cookiy workflows can trigger paid recruitment, checkout, report generation, or administrative links. <br>
Mitigation: Require explicit user confirmation before any paid, checkout, report-generation, recruitment, or admin-link action, and show payment quotes before proceeding. <br>
Risk: External study and survey operations may affect real participants or generate misleading research conclusions if launched without review. <br>
Mitigation: Confirm participant criteria, countries, languages, study materials, and survey design with the user before launch, then review generated reports before acting on findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chenglin97/user-research-cookiy) <br>
- [Cookiy agent introduction](https://cookiy.ai/intro-for-agent.txt) <br>
- [Cookiy workflow reference](references/cookiy/cookiy.md) <br>
- [Cookiy qualitative research reference](references/cookiy/cookiy-qual.md) <br>
- [Cookiy quantitative survey reference](references/cookiy/cookiy-quant.md) <br>
- [Cookiy recruitment reference](references/cookiy/cookiy-recruit.md) <br>
- [Cookiy billing reference](references/cookiy/cookiy-billing.md) <br>
- [Qualitative research planner](references/qualitative-research-planner/qualitative-research-planner.md) <br>
- [Research report synthesis workflow](references/synthesize-research-report/synthesize-research-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Cookiy CLI commands, study or survey JSON, research plans, interview guides, transcripts summaries, and reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
