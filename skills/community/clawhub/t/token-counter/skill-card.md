## Description: <br>
Track and analyze OpenClaw token usage across main, cron, and sub-agent sessions with category, client, model, and tool attribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mkhaytman87](https://clawhub.ai/user/mkhaytman87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to inspect local OpenClaw token usage, drill into sessions, and identify category, client, model, and tool-level cost drivers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw transcripts and session metadata that may contain private prompts, file paths, timestamps, client names, tool usage, and other sensitive context. <br>
Mitigation: Use explicit data paths, run it only on workspaces whose transcripts may be inspected, and keep generated reports private. <br>
Risk: Saved JSON reports can persist derived session details beyond the original transcript location. <br>
Mitigation: Review saved reports before sharing and delete snapshots that are no longer needed. <br>
Risk: Tool token attribution is heuristic and may not exactly match billing records. <br>
Mitigation: Use attribution as a hotspot guide and confirm important cost decisions against authoritative billing or platform usage data. <br>


## Reference(s): <br>
- [Token Counter on ClawHub](https://clawhub.ai/mkhaytman87/token-counter) <br>
- [Classification Rules](references/classification-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, json, markdown, shell commands, guidance] <br>
**Output Format:** [Plain text reports or JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write reports to a selected output path or save daily JSON snapshots.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
