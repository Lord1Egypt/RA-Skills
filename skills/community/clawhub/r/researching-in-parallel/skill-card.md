## Description: <br>
Research any topic thoroughly by running three sub-agents with distinct analytical lenses, then giving their outputs to a final sub-agent to produce or update a review report with a unified bibliography. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vsamtani](https://clawhub.ai/user/vsamtani) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, analysts, and teams use this skill when they need a deep, multi-perspective research report or an update to an existing report. It coordinates breadth, critical, and evidence passes, then synthesizes their findings into a report and bibliography. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Parallel sub-agents perform web research and write prompts, reports, bibliographies, and optional source extracts into a workspace. <br>
Mitigation: Use a new empty workspace, provide only sources the agents should read, and review generated files before relying on them. <br>
Risk: AI-generated research may include incorrect claims, gaps, or citations that need verification. <br>
Mitigation: Independently verify important citations and use the generated bibliography and source extracts as review aids, not as final authority. <br>


## Reference(s): <br>
- [Configuration Reference](references/configuration.md) <br>
- [Report Template](assets/report-template.md) <br>
- [Bibliography Template](assets/bibliography-template.md) <br>
- [Original Parallel Research Method](https://www.bleeta.ai/post/your-30-minute-ai-research-system-a-practical-guide) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files, Guidance] <br>
**Output Format:** [Markdown reports, bibliography files, source extracts, prompt files, and concise chat status with file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May spawn multiple sub-agents and save reusable source extracts when configured.] <br>

## Skill Version(s): <br>
1.4.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
