## Description:

Searches, briefs, and monitors Korean used-market listings across Daangn, Bunjang, and Joonggonara using natural-language search and watch rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[twbeatles](https://clawhub.ai/user/twbeatles)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search Korean second-hand marketplaces, receive concise listing briefings, and create persistent watch rules for new listings or price drops.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill emits shell and cron command strings that can include user-controlled rule names.

Mitigation: Review scheduled jobs before enabling them and have automation call the script with argument arrays or properly escaped arguments.

Risk: Search terms are sent to marketplace and search sites during listing checks.

Mitigation: Install and operate the skill only when sending those search terms to the supported sites is acceptable.

Risk: Watch state is stored locally and may contain monitored item names, listing links, prices, and event history.

Mitigation: Protect or periodically clean data/watch-rules.json according to the operator's retention and privacy needs.

## Reference(s):

- [Upstream notes](references/upstream-notes.md)
- [ClawHub skill page](https://clawhub.ai/twbeatles/skills/used-market-watch)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text or JSON with listing summaries, watch events, recommended commands, and cron payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local watch rules, event history, and last-seen listing state to data/watch-rules.json.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
