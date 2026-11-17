## Description:

Voice2notion transcribes voice recordings with faster-whisper, extracts key information, and saves the results to a Notion database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiabaochen1](https://clawhub.ai/user/jiabaochen1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn voice notes, meetings, and discussions into structured Notion database records with transcripts, topics, key points, tasks, dates, and recording links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive audio or transcripts may be exposed when recordings are stored through public links.

Mitigation: Use private or expiring access-controlled storage for recordings and avoid public recording links.

Risk: A broadly scoped Notion integration could expose more workspace data than the workflow requires.

Mitigation: Use a narrowly scoped Notion integration and share only the target database with that integration.

Risk: Unpinned transcription dependencies may change behavior across installations.

Mitigation: Install faster-whisper in a dedicated virtual environment and pin dependency versions before operational use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jiabaochen1/skills/voice2notion)
- [Notion Database Template](https://www.notion.so/4e667ba767e2414a9f89041471d5f85d)
- [Notion Integrations](https://www.notion.so/my-integrations)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces transcription workflow guidance, Notion configuration instructions, database field guidance, and example commands.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
