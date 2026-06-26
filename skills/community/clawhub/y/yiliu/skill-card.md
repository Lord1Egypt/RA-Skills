## Description: <br>
Yiliu is an AI-powered note-taking knowledge base with semantic search, auto-summarization, tagging, version history, and Markdown export. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DamingDong](https://clawhub.ai/user/DamingDong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to capture personal notes, search them by keyword or semantic intent, inspect version history, view statistics, and export notes to Markdown. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores captured notes locally, which can retain sensitive personal or work information. <br>
Mitigation: Avoid storing highly sensitive material unless the local storage model is acceptable, and review stored/exported notes before sharing or backing them up. <br>
Risk: When OPENAI_API_KEY is configured, note text and search queries may be sent to the configured AI endpoint. <br>
Mitigation: Use AI features only with an endpoint you trust, and leave OPENAI_API_KEY unset when local-only behavior is required. <br>
Risk: Broad activation rules and automatic processing may capture or process more note content than a user expects. <br>
Mitigation: Use explicit Yiliu commands for note capture, verify content before saving or exporting, and handle delete/export commands carefully. <br>


## Reference(s): <br>
- [Yiliu ClawHub Listing](https://clawhub.ai/DamingDong/yiliu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Text and Markdown, with command-oriented responses and optional Markdown export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores notes locally and may call a configured OpenAI-compatible endpoint when OPENAI_API_KEY is set; otherwise core recording and search functions can operate with local fallback behavior.] <br>

## Skill Version(s): <br>
1.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
