## Description:

每日笔记深度解读。从笔记目录筛选当日笔记，分类、逐条提炼要点，最后做深度关联分析和洞察挖掘。

This skill is ready for commercial/non-commercial use.

## Publisher:

[youngandsure](https://clawhub.ai/user/youngandsure)

### License/Terms of Use:

MIT-0

## Use Case:

Users with a configured notes directory use this skill to find notes modified today, group them by topic, summarize each note, and produce a deeper report that connects current notes with relevant historical notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill searches across the configured notes directory, including older notes, and analyzes matched note contents.

Mitigation: Set NOTES_DIR only to a folder whose notes are appropriate to expose for analysis, and narrow the folder before use when sensitive notes are present.

Risk: Generated keywords may be inserted into a grep pattern without escaping.

Mitigation: Review or escape generated keywords before running grep commands, especially when keywords contain shell or regular-expression metacharacters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/youngandsure/skills/summarize-notes)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown report with tables, per-note summaries, deep analysis, and historical-note connections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured NOTES_DIR and may search Markdown or text notes recursively.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
