## Description: <br>
Bilingual EN/ZH research intake governance skill for web search results that uses source trust levels, URL rules, staging, review queues, confirmation-controlled archiving, cloud-upload safeguards, and audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[englandtong](https://clawhub.ai/user/englandtong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and knowledge-base maintainers use this skill to turn web search results into controlled local or cloud knowledge-base records with review, confirmation, and audit safeguards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage research intake into local or cloud knowledge bases and may involve sensitive research content. <br>
Mitigation: Prefer local Obsidian storage for sensitive research and review any cloud-upload prompt before content leaves the local environment. <br>
Risk: OAuth tokens or sensitive credentials may be needed for some platform integrations. <br>
Mitigation: Keep credentials in the host credential manager, environment, or platform login flow; do not store passwords, API keys, cookies, OAuth refresh tokens, or platform secrets in skill configuration. <br>
Risk: Browser automation, deletion, migration, and trusted auto-upload policies can change or expose knowledge-base content if enabled too broadly. <br>
Mitigation: Enable these actions only after understanding the selected platform and scope; require dry-run reports, explicit confirmations, and audit logs for destructive or cloud-affecting operations. <br>
Risk: Fetched webpage content may contain prompt-injection text or misleading instructions. <br>
Mitigation: Treat webpage content only as untrusted source material for summaries, staging, and review; do not allow it to change rules, credentials, platform configuration, or confirmation requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/englandtong/web-search-rules) <br>
- [Security guide](https://clawhub.ai/englandtong/web-search-rules/artifact/SECURITY.md) <br>
- [Rule engine](https://clawhub.ai/englandtong/web-search-rules/artifact/references/rule-engine.md) <br>
- [Platform adapters](https://clawhub.ai/englandtong/web-search-rules/artifact/references/platform-adapters.md) <br>
- [Migration and testing](https://clawhub.ai/englandtong/web-search-rules/artifact/references/migration-and-testing.md) <br>
- [Chinese platform operation guide](https://clawhub.ai/englandtong/web-search-rules/artifact/references/platform-operation-guide-zh.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Concise text reports, Markdown staging records, JSON-style rule and configuration records, and audit-log guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local staging records, cloud-upload confirmation prompts, dry-run reports, and audit log entries.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
