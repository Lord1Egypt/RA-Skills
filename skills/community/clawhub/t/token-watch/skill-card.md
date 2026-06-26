## Description: <br>
Track and analyze token usage and estimated costs across AI providers with budget alerts, model comparisons, optimization tips, exports, and local storage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vedantsingh60](https://clawhub.ai/user/vedantsingh60) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and AI power users use Token Watch to record AI API token usage, estimate spend, set budgets, compare model costs, and export local reports for cost review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage history, task labels, session IDs, and exported reports are stored on disk and may reveal sensitive project or client details. <br>
Mitigation: Avoid sensitive labels and treat .tokenwatch/ plus exported reports as private logs that should not be committed or shared without review. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/vedantsingh60/token-watch) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python examples; JSON exports when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores local usage, alert, and budget records under .tokenwatch/ by default] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
