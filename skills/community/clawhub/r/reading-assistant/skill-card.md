## Description:

個人閱讀助理，用於管理 EPUB 電子書圖書館、生成章節摘要並追蹤閱讀進度。

This skill is ready for commercial/non-commercial use.

## Publisher:

[justine-nl](https://clawhub.ai/user/justine-nl)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to import EPUB books, organize a personal reading library, create chapter summaries, and track reading progress. It can also provide reading-list status, continuation prompts, optional Notion synchronization, and cron-based reading reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted book text, progress data, and generated summaries are stored persistently under the OpenClaw workspace.

Mitigation: Install only if local storage of book content and summaries is acceptable, and review workspace retention or deletion practices before importing books.

Risk: Optional Notion synchronization and cron reminders may send summaries or progress information outside the local workspace.

Mitigation: Enable Notion sync or scheduled reminders only after confirming the destination, delivery channel, and how to disable the automation.

Risk: The skill has broad natural-language triggers that could activate around general reading or book-related requests.

Mitigation: Review assistant behavior after installation and require explicit confirmation before importing books, updating progress, or sending reminders.

Risk: The EPUB import workflow installs Python dependencies at runtime.

Mitigation: Use a virtual environment or pinned dependencies for the EPUB processing workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/justine-nl/skills/reading-assistant)
- [Publisher profile](https://clawhub.ai/user/justine-nl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown responses with JSON progress data and generated text files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local manifests, chapter text files, progress records, reading summaries, and optional automation or sync guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
