## Description: <br>
Strict Father is a Ziwei Doushu 12-palace self-analysis skill that asks for birth details, computes a chart, and produces direct behavioral blind-spot analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcii](https://clawhub.ai/user/0xcii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for structured self-reflection based on Ziwei Doushu chart data, behavioral history, and direct diagnostic prompts. It is aimed at users seeking personal blind-spot analysis rather than general counseling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installation flow can download files and install npm packages, including through a curl-to-shell command. <br>
Mitigation: Use manual installation, inspect the downloaded files first, and install dependencies only from trusted sources. <br>
Risk: The skill asks for exact birth details and can reuse chart data for later sessions or reminders without clearly documented storage or deletion behavior. <br>
Mitigation: Provide birth details only if comfortable with reuse in future analysis, and avoid enabling reminders or external delivery destinations unless their privacy handling is understood. <br>
Risk: The skill uses a deliberately forceful diagnostic persona that may produce harsh personal feedback. <br>
Mitigation: Treat outputs as self-reflection prompts, not clinical, financial, legal, or medical advice, and avoid using the skill with vulnerable users without additional safeguards. <br>


## Reference(s): <br>
- [Strict Father ClawHub listing](https://clawhub.ai/0xcii/strict-father-v2) <br>
- [Publisher profile](https://clawhub.ai/user/0xcii) <br>
- [12-palace behavior pattern matrix](references/palace-pattern-matrix.md) <br>
- [Author contact](https://t.me/yongzhuan_bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with structured text and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call a local Node.js chart calculation script that returns JSON before producing human-readable analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
