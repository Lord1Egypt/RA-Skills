## Description:

Voice Memory Features helps voice and phone agents store and recall conversations, journal entries, CRM interactions, meetings, coaching progress, and sales follow-ups through BlueColumn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams building voice, phone, meeting, CRM, coaching, sales, or journaling agents use this skill to add conversation memory, recall context before responses, and make transcripts or notes searchable through BlueColumn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice, meeting, journal, CRM, coaching, and sales content may be uploaded to BlueColumn and made searchable later.

Mitigation: Require explicit opt-in, minimize stored content, prefer summaries where full transcripts are not needed, and provide redaction, retention, and deletion controls.

Risk: Recalled memory could carry unsafe, stale, or prompt-injection content into a voice agent response.

Mitigation: Do not place recalled memory in a system prompt; keep it scoped as reviewable context and validate it before taking action.

Risk: A misconfigured memory endpoint or broad API key could expose sensitive conversation data.

Mitigation: Lock BLUECOLUMN_BASE to a trusted HTTPS endpoint and use a narrowly scoped BlueColumn API key.

## Reference(s):

- [BlueColumn API Documentation](https://bluecolumn.ai/docs)
- [ClawHub Skill Page](https://clawhub.ai/bluecolumnconsulting-lgtm/skills/voice-memory-features)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key for live memory storage and recall; included tests mock network calls.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
