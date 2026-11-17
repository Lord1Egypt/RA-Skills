## Description:

Find, read and cite the owner's Zoom meetings through zm - search stored transcripts, summaries and meeting chat, read what was said around a hit, list meetings and cloud recordings, archive recordings, prepare for an upcoming meeting, and create, change or cancel a Zoom meeting when the owner asks. Use when a question could be answered from Zoom calls (what someone said, decided or promised, when a topic came up, who took part), when asked to find a Zoom meeting, recording or transcript, summarise a call, prepare for a meeting, or sign in to Zoom. Not for joining calls or operating the Zoom desktop client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Zoom account owners and their assistants use this skill to find, review and cite meeting transcripts, summaries, chat and recordings, prepare for meetings, and make specifically authorized meeting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search and contact lookup can reach beyond Zoom meetings, including broader communications and contact sources.

Mitigation: Use only sources explicitly configured for the selected profile and keep searches within the owner's request.

Risk: Remote-model search can send transcript passages to an external model.

Mitigation: Use offline or local inference when transcript text must stay on the machine; do not send credentials in endpoint URLs.

Risk: Creating, changing or cancelling a Zoom meeting changes the owner's remote schedule.

Mitigation: Make only the exact change the owner requested, ask the owner before MCP writes, and inspect Zoom before retrying an uncertain dispatched write.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wirecat/skills/wirecat-zoom)
- [Search and read meetings](artifact/references/search.md)
- [People, projects, filters and tags](artifact/references/people-and-projects.md)
- [Preparing for an upcoming meeting](artifact/references/prepare.md)
- [Recordings, archive and ingestion](artifact/references/archive.md)
- [Meetings and contacts in Zoom](artifact/references/zoom-live.md)
- [Sign-in, Zoom app and MCP](artifact/references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Text or Markdown with cited meeting references and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserve source references and coverage; search results may be incomplete.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
