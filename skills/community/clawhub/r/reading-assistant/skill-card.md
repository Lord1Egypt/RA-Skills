## Description: <br>
個人閱讀助理，協助使用者匯入 EPUB、管理電子書圖書館、產生章節摘要並追蹤閱讀進度。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Justine-NL](https://clawhub.ai/user/Justine-NL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users use this skill to organize a personal EPUB library, import books, generate chapter-level summaries, and keep track of reading progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: EPUB contents, generated summaries, and reading history may be stored in the OpenClaw workspace. <br>
Mitigation: Install only if local storage of private reading data is acceptable, and keep the workspace protected. <br>
Risk: Optional Notion sync can send book metadata, summaries, and reading progress to an external service. <br>
Mitigation: Enable Notion sync only when that sharing is intended and the connected workspace is appropriate for the data. <br>
Risk: Cron reminders can automatically summarize the next chapter and push reading content to messaging platforms. <br>
Mitigation: Enable the cron reminder only after reviewing the schedule, prompt, and destination, and disable it when unattended sharing is not desired. <br>
Risk: Broad reading-related triggers may activate the skill during ordinary book or summary requests. <br>
Mitigation: Review actions that import files, read chapters, update progress, or send summaries before allowing them to proceed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Justine-NL/reading-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with JSON files and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores EPUB-derived chapter text, manifests, summaries, and reading progress in the local OpenClaw workspace; optional Notion sync and cron reminders may send reading data to external services.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
