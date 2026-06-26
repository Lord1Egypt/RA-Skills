## Description: <br>
Token Pilot helps OpenClaw agents reduce token usage with behavioral rules, plugin synergy guidance, workspace analysis, and audit or optimization commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[beyound87](https://clawhub.ai/user/beyound87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inject and apply token-saving operating rules, audit workspace and agent configurations, and generate recommendations for lower-cost agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initialization flow can persistently change all local OpenClaw agents by appending or replacing Token Pilot rules in AGENTS.md files. <br>
Mitigation: Review the initialization preview, confirm affected agents before writing, and avoid --yes unless unattended bulk changes are intentional. <br>
Risk: The optional optimization apply mode can move or delete workspace files. <br>
Mitigation: Run read-only audit or optimization modes first, review proposed changes, and back up workspace files before using --apply. <br>
Risk: Persistent memory and workspace files can accidentally retain sensitive user data while applying token-saving memory practices. <br>
Mitigation: Keep secrets and sensitive user data out of persistent memory files and review memory cleanup recommendations before applying them. <br>


## Reference(s): <br>
- [Token Pilot Skill Page](https://clawhub.ai/beyound87/token-pilot) <br>
- [Token Pilot Core Rules](references/TOKEN-PILOT-CORE.md) <br>
- [Cron Job Token Optimization](references/cron-optimization.md) <br>
- [Workspace File Organization for Minimal Token Cost](references/workspace-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include read-only audit summaries, initialization previews, and optional workspace cleanup recommendations.] <br>

## Skill Version(s): <br>
3.8.0 (source: server release metadata; artifact frontmatter and README report 3.6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
