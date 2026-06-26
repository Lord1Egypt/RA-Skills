## Description: <br>
Monitors computer activity with periodic screenshots and OCR, then generates daily review reports with ROI analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drpris](https://clawhub.ai/user/drpris) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and knowledge workers use this skill to run local screen activity monitoring, extract screen text, review time allocation, and generate daily productivity reports. It is useful when a user wants time tracking, activity logs, ROI analysis, or a Chinese-language daily review workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill captures and OCRs full-screen activity, which can include passwords, private messages, regulated work, or other sensitive content. <br>
Mitigation: Review ~/.screen-reviewer/config.yaml before starting, expand the app blacklist, grant screen permissions only intentionally, and pause or stop monitoring during sensitive work. <br>
Risk: Screen-derived summaries may be sent to configured cloud AI providers when reports are generated. <br>
Mitigation: Use a local provider such as Ollama when possible, or avoid configuring cloud API keys unless off-device processing is acceptable. <br>
Risk: Screenshots, logs, and reports are retained locally and the service can persist at login. <br>
Mitigation: Use the provided cleanup, stop, and uninstall commands when monitoring is not needed, and manually delete retained logs or reports when required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drpris/screen-reviewer) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Daily review prompt](artifact/templates/review_prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, command guidance, configuration notes, and local log/report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local screenshots, JSONL activity logs, and daily review reports under ~/.screen-reviewer when the monitoring service is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
