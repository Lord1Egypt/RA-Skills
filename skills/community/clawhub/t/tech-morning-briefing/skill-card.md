## Description: <br>
Tech Morning Briefing collects technology news daily, scores and categorizes items, and produces a curated Feishu morning brief with an archive document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uuoov](https://clawhub.ai/user/uuoov) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams that use OpenClaw and Feishu use this skill to automate a daily technology-news briefing for chat delivery and document archiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured Feishu destination could post the briefing or archive entries to the wrong chat or document. <br>
Mitigation: Confirm the Feishu chat, document destination, owner permissions, and cron target before enabling the daily job. <br>
Risk: The skill stores a Feishu document token in local runtime configuration. <br>
Mitigation: Keep data/config.json private, avoid committing runtime data, and restrict filesystem access to trusted operators. <br>
Risk: Automated search, scoring, and summarization can include stale, low-quality, or misleading news items. <br>
Mitigation: Review the briefing output before relying on it for external communications or business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uuoov/tech-morning-briefing) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Tavily](https://tavily.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing grouped by category, with Feishu chat messages and appended archive entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local runtime state for the news pool, quote rotation, and Feishu document token.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
