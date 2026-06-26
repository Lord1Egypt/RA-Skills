## Description: <br>
Trading Coach analyzes broker CSV trade records, matches positions with FIFO logic, scores trading quality across multiple dimensions, and produces review insights and improvement guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BENZEMA216](https://clawhub.ai/user/BENZEMA216) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to turn broker CSV exports into trading performance reviews, quality scores, and actionable coaching suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run unreviewed external code on sensitive brokerage CSV files. <br>
Mitigation: Review the referenced repository and dependencies before running it, use a virtual environment or other isolation, and run only copied CSVs with account identifiers and unnecessary personal data removed. <br>
Risk: Generated scores and recommendations could be mistaken for trading instructions. <br>
Mitigation: Treat generated analysis as informational coaching output and review it before making trading decisions. <br>


## Reference(s): <br>
- [Trading Coach on ClawHub](https://clawhub.ai/BENZEMA216/trading-coach) <br>
- [Supported CSV Formats](artifact/references/csv_formats.md) <br>
- [AI Insight Dimensions](artifact/references/insight_dimensions.md) <br>
- [Quality Scoring System](artifact/references/scoring_system.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and structured trading-review recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask the agent to run local Python commands against user-provided broker CSV files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
