## Description: <br>
Search, brief, and monitor Korean used-market listings across Danggeun Market, Bunjang, and Joonggonara from natural-language requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[twbeatles](https://clawhub.ai/user/twbeatles) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and automation agents use this skill to search Korean used-market listings, summarize results, save watch rules, and check for new listings or price drops. It is suited for chat-driven marketplace monitoring where a higher-level scheduler or messaging layer handles delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Marketplace search terms are sent to third-party sites during Playwright-based searches. <br>
Mitigation: Use only search terms the user is comfortable sending to those sites, and avoid sensitive personal or confidential queries. <br>
Risk: Watch rules and event history are saved locally in data/watch-rules.json. <br>
Mitigation: Review stored watch state for sensitive terms and remove stale or unnecessary rules with the skill's watch management commands. <br>
Risk: Automation output can include shell, cron, persist, or system-event command strings derived from user-controlled text. <br>
Mitigation: Review generated commands before scheduling or execution, and pass arguments without blind shell evaluation when integrating with another agent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/twbeatles/used-market-watch) <br>
- [Upstream notes](references/upstream-notes.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Korean text briefings or structured JSON with optional cron and system-event command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local watch state to data/watch-rules.json when watch rules are saved or checked.] <br>

## Skill Version(s): <br>
0.4.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
