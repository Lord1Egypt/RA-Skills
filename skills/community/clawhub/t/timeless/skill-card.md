## Description:

Query and manage Timeless meetings, rooms, transcripts, and AI documents, and capture podcast episodes or YouTube videos into Timeless for transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eilonmore](https://clawhub.ai/user/eilonmore)

### License/Terms of Use:


## Use Case:

Employees, external users, developers, and agents use this skill to search and read Timeless meeting content, retrieve transcripts and AI-generated documents, manage rooms, upload recordings, and bring podcast or YouTube media into Timeless for transcription.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access and move sensitive Timeless meeting data, including transcripts, recordings, summaries, participants, and room contents.

Mitigation: Store TIMELESS_ACCESS_TOKEN as a secret, avoid exposing it in chats or logs, and confirm with the user before exports, uploads, room mutations, or automations that process meeting data.

Risk: Upload and capture workflows can send selected local recordings, podcast episodes, or YouTube downloads to Timeless for transcription.

Mitigation: Require explicit confirmation before uploads, use trusted public media URLs, and keep downloads in safe temporary directories that are cleaned up after use.

Risk: The documented Timeless API endpoints are described as internal and may change without notice.

Mitigation: Check API responses and status codes at runtime, handle authentication failures and rate limits, and avoid relying on unattended automation without monitoring.

## Reference(s):

- [Timeless Skill Homepage](https://github.com/supertools/timeless-skills)
- [Timeless](https://timeless.day)
- [Timeless API Token Page](https://my.timeless.day/api-token)
- [Timeless Unofficial API Reference](artifact/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples, API request examples, and JSON response handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that read or mutate Timeless account data, upload local recordings, download public media, or configure polling automations.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
