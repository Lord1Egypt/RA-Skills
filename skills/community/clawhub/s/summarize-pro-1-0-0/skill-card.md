## Description:

Summarize Pro helps an agent summarize text, articles, documents, meetings, emails, transcripts, reports, conversations, and other long-form content in multiple concise formats while operating locally without artifact evidence of network access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xvolica](https://clawhub.ai/user/xvolica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn long content into TL;DRs, bullet summaries, executive summaries, action items, meeting notes, email summaries, comparison summaries, translated summaries, and custom-length summaries. It can also maintain local summary history, saved summaries, preferences, templates, and usage statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local summary metadata, statistics, saved summaries, templates, topics, timestamps, and word counts under ~/.openclaw/summarize-pro/.

Mitigation: Avoid summarizing sensitive content if those local records are unacceptable, or periodically review and delete the local data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xvolica/skills/summarize-pro-1-0-0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries with structured headings, lists, tables, and word-count statistics]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local JSON files for settings, history, saved summaries, templates, and usage statistics under ~/.openclaw/summarize-pro/.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
