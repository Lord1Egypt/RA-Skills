## Description: <br>
Daily briefing that connects your recent reading to your long-term archive. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sameerbajaj](https://clawhub.ai/user/sameerbajaj) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to turn recent Readwise Reader saves into a WhatsApp briefing that connects current reading themes with older archive items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Readwise reading history, summaries, URLs, and inferred interests may be processed by the configured LLM and sent through WhatsApp. <br>
Mitigation: Install only if that data flow is acceptable; verify the WhatsApp recipient, token storage, and included fields before enabling automation. <br>
Risk: Scheduled runs can repeatedly process new saves and send briefings without per-run review. <br>
Mitigation: Test the script manually before adding cron, review the generated briefing path, and disable or update the schedule when recipient or model routing changes. <br>


## Reference(s): <br>
- [Reader Deep Dive on ClawHub](https://clawhub.ai/sameerbajaj/reader-deep-dive) <br>
- [Readwise Access Token](https://readwise.io/access_token) <br>
- [Readwise Reader list API endpoint](https://readwise.io/api/v3/list/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [WhatsApp-friendly text with lightweight Markdown-style emphasis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires READWISE_TOKEN and TARGET_NUMBER; uses curl, jq, gemini, and clawdbot to fetch Readwise data, synthesize a briefing, and send it to WhatsApp.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
