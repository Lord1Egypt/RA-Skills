## Description: <br>
Guides an agent to use the Ultrahuman MCP to answer questions about sleep, recovery, readiness, daily metrics, ring data, glucose, and metabolic health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Duzafizzl](https://clawhub.ai/user/Duzafizzl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Ultrahuman users and their agents use this skill to turn account health data into morning briefs, recovery checks, daily metric summaries, and short multi-day sleep or glucose trend comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch sensitive biometric and health-related account data through the configured Ultrahuman MCP server. <br>
Mitigation: Use it only with a trusted MCP server and account, and require user confirmation before fetching data for broad wellness prompts. <br>
Risk: Sleep, recovery, and glucose summaries could be mistaken for medical advice. <br>
Mitigation: Keep responses descriptive, avoid diagnoses or treatment advice, and present interpretation heuristics as non-medical orientation. <br>


## Reference(s): <br>
- [Interpreting Ultrahuman metrics](references/interpretation.md) <br>
- [Ultrahuman metrics glossary](references/metrics_glossary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Concise Markdown summaries with metric lists, short tables, and descriptive recommendations when appropriate.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include date-specific or multi-day metric comparisons; avoids medical diagnoses and raw JSON unless requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
