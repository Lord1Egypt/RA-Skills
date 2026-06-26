## Description: <br>
每天抓取 Clawhub 热门技能，深入分析并生成报告。每次执行获取一个未分析过的热门技能，避免重复。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[autoxj](https://clawhub.ai/user/autoxj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users run this skill to analyze one unprocessed trending ClawHub skill at a time and save a daily Markdown report. It is useful for recurring marketplace research without requiring a ClawHub account or API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The runner contacts ClawHub with Playwright and Chromium and creates local report and state files. <br>
Mitigation: Run it only in an environment where ClawHub access and local file creation are acceptable. <br>
Risk: Generated reports may include local sibling skill directory paths and filenames. <br>
Mitigation: Review generated reports before sharing them outside the local environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/autoxj/skill-everyday) <br>
- [ClawHub skills directory](https://clawhub.ai/skills) <br>
- [Playwright installation guide](https://playwright.dev/docs/intro) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [Markdown reports written to data/reports with terminal summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local state in data/analyzed.json and writes both dated reports and data/reports/LATEST.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
