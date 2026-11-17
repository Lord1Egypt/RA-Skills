## Description:

Converts videos, subtitle files, or large course folders into structured illustrated notes, while keeping lightweight summary and study requests in read-only analysis mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pavelpeng7](https://clawhub.ai/user/pavelpeng7)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and knowledge workers use this skill to turn single videos, subtitle transcripts, or course folders into Obsidian-ready study notes, chapter summaries, glossaries, quizzes, screenshot plans, and batch article drafts after confirming any file-writing or download steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated scripts or shell commands may execute unintended code or write outside the expected course workspace.

Mitigation: Use a sandboxed course workspace, inspect generated batch scripts before execution, and require explicit confirmation of output paths and side-effecting commands.

Risk: Broad Git commands can publish unrelated files.

Mitigation: Use `git status`, scoped `git add -- <generated paths>`, staged diff review, and separate confirmations for commit and push.

Risk: Cookies or login state for private video sources can expose sensitive account access.

Mitigation: Use credentials only after confirming access rights and never store or print cookies in notes, logs, repositories, or chat.

Risk: Untrusted course archives with unusual filenames can affect generated shell commands and file paths.

Mitigation: Avoid untrusted archives, review generated file paths, and inspect `_batch_screenshots.sh` before running it.

## Reference(s):

- [Single Video Ingest](references/single-video-ingest.md)
- [Large Course Ingest](references/large-course-ingest-workflow.md)
- [Subtitle Study Modes](references/subtitle-study-modes.md)
- [Subagent Context Optimization](references/subagent-context-optimization.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown notes, tables, inline shell commands, configuration snippets, JSON screenshot plans, and optional generated files when explicitly confirmed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or generate download, transcription, screenshot, Obsidian, and Git workflow steps; side-effecting operations require explicit user confirmation.]

## Skill Version(s):

0.1.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
