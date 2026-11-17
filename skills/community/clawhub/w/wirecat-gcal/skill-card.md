## Description:

Use gcal, a Google Calendar CLI from WireCat, from an agent with the owner's profile and JSON answers. Use when a question could be answered from the owner's Google Calendar (what is on today or this week, when a meeting is, who comes, when people are free, what changed or clashes), to prepare a meeting brief or a daily or weekly digest from the local store, to read Google Meet calls with who joined, their transcripts and Drive files, to create, change or delete an event (with a Meet link) or answer an invitation when the owner asks, or to call any Calendar API method through gcal api.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use the owner's signed-in Google Calendar profile to answer schedule and availability questions, prepare meeting briefs and digests, review Google Meet details, and make calendar changes the owner requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags access to shared messages and notes beyond calendar work; its verdict is suspicious and scanner coverage is partial.

Mitigation: Before installing, consider whether access to shared messages and notes fits your needs. Treat invitation, message, note, and transcript text from others as untrusted data, not instructions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wirecat/skills/wirecat-gcal)
- [Reading events](artifact/references/events.md)
- [Meeting briefs and digests](artifact/references/prepare.md)
- [Changing events](artifact/references/changing.md)
- [Google Meet calls](artifact/references/meet.md)
- [Calendars, feeds and reminders](artifact/references/calendars.md)
- [The Calendar API](artifact/references/api.md)
- [gcal over MCP](artifact/references/mcp.md)
- [Remote MCP setup guide](https://github.com/WireCatLabs/gcal-cli/blob/main/docs/remote.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [JSON command results and concise text or Markdown answers, meeting briefs, and calendar digests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Answers may be incomplete when calendar or meeting data is unavailable; report completeness information returned by the skill.]

## Skill Version(s):

1.0.7 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
