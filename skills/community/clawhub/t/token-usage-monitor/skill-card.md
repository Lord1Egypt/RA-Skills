## Description: <br>
Monitors AI model token usage, historical trends, threshold alerts, and cost estimates to help control AI service expenses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ttjsndx](https://clawhub.ai/user/ttjsndx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to track token consumption, review usage history, set usage thresholds, and estimate AI model costs for sessions and applications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill retains session IDs, model names, timestamps, usage totals, and estimated costs as local operational metadata. <br>
Mitigation: Install only where local retention is acceptable, restrict access to the local usage file, and avoid sharing it outside approved workflows. <br>
Risk: Adding chat, email, or webhook alerts could expose token usage metadata outside the local environment. <br>
Mitigation: Review alert-channel changes before enabling them and send only the minimum usage data needed. <br>


## Reference(s): <br>
- [Token Usage Monitor Integration Guide](references/integration_guide.md) <br>
- [ClawHub package page](https://clawhub.ai/ttjsndx/token-usage-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled Python script records usage data in local JSON storage and prints reports, alerts, and summaries to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
