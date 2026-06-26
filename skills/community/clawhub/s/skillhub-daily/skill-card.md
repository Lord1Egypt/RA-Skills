## Description: <br>
SkillHub Daily scans SkillHub rankings and category data, matches skills to user pain points, and produces personalized daily recommendations that can be saved to IMA, Lark/Feishu, Obsidian, or local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[edwardwason](https://clawhub.ai/user/edwardwason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to receive daily SkillHub recommendations matched to stated or memory-derived pain points, with optional scheduled delivery and storage. It is useful for discovering high-value agent skills across SkillHub categories without manually browsing rankings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local memory or log context for personalization. <br>
Mitigation: Use Cron prompts with explicit pain points when memory scanning is not desired, and authorize only the context sources needed for the report. <br>
Risk: The skill can reuse IMA credentials from environment variables or local configuration files. <br>
Mitigation: Use dedicated least-privilege IMA credentials, protect config.json files, and avoid shared credentials across unrelated skills. <br>
Risk: The skill can send generated reports to external destinations such as IMA, Lark/Feishu, or Obsidian paths. <br>
Mitigation: Verify each destination and storage channel before enabling scheduled delivery. <br>
Risk: TLS verification can be disabled for IMA push behavior through configuration. <br>
Mitigation: Leave TLS verification enabled and review any exception before running scheduled delivery. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/edwardwason/skillhub-daily) <br>
- [Setup wizard](references/setup-wizard.md) <br>
- [Configuration guide](references/config.md) <br>
- [Prompt templates](references/prompt-templates.md) <br>
- [Briefing template](references/briefing-template.md) <br>
- [Source contract](references/source-contract.md) <br>
- [Platform adapters](references/platform-adapters.md) <br>
- [SkillHub API](https://api.skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown briefings and summaries, JSON data snapshots, and shell/configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create dated reports under data/reports and snapshots under data/snapshots; optional delivery depends on configured external destinations.] <br>

## Skill Version(s): <br>
6.2.1 (source: server release evidence; artifact metadata reports 6.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
