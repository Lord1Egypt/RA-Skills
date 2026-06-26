## Description: <br>
Analyzes writing for grammar, style, tone, readability, and consistency while learning user preferences over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to review, rewrite, and coach prose across emails, reports, blog posts, resumes, and other documents. It produces grammar, style, tone, readability, and consistency feedback while maintaining a persistent local style profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store long-term writing metadata, session summaries, and reports locally, and some session history may include excerpts from submitted text. <br>
Mitigation: Treat the local data directory as sensitive, review stored files periodically, and clear ~/.openclaw/skills/writing-coach-pro/data when retention is not needed. <br>
Risk: Dashboard sync is enabled by default for writing statistics and trend data. <br>
Mitigation: Review the dashboard settings before use and disable dashboard sync when writing analytics should remain local or should not be retained. <br>
Risk: Submitted text is processed by whichever LLM backend the host agent uses, which may be a cloud service. <br>
Mitigation: Use a local model for confidential drafts or review the configured LLM provider's data handling terms before submitting sensitive text. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nollio/writing-coach-pro) <br>
- [Security information](artifact/SECURITY.md) <br>
- [Setup guide](artifact/SETUP-PROMPT.md) <br>
- [Dashboard integration spec](artifact/dashboard-kit/DASHBOARD-SPEC.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, inline text feedback, rewritten prose, shell command guidance, and JSON-backed configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist style preferences, session summaries, writing metrics, and generated reports in local skill data directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
