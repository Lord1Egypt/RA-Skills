## Description: <br>
Summarize Pro helps an agent summarize text, articles, documents, meetings, emails, transcripts, reports, conversations, and other long content in formats such as bullets, TL;DR, ELI5, key takeaways, action items, executive summaries, comparisons, translations, and custom-length summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xvolica](https://clawhub.ai/user/xvolica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert long or dense content into concise summaries, action items, takeaways, comparisons, and language-specific summaries. The skill also supports local summary history, saved summaries, templates, preferences, and usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores preferences, statistics, saved summaries, templates, and recent summary history locally, which may include sensitive metadata or summary content. <br>
Mitigation: Use it only on content appropriate for local retention, and periodically review or clear ~/.openclaw/summarize-pro/ when handling sensitive material. <br>
Risk: Broad summary-related activation phrases can trigger the skill when a user intended only a casual or unrelated request. <br>
Mitigation: Confirm the summarization task and target content before creating or updating local summary history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/xvolica/summarize-pro-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown summaries with local JSON configuration and history files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files under ~/.openclaw/summarize-pro/ for preferences, stats, saved summaries, templates, and recent summary history.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
