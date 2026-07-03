## Description: <br>
Generates structured learning notes from AI coding sessions, including code explanations, knowledge points, review prompts, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyqqqq66666](https://clawhub.ai/user/lyqqqq66666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and developers use this skill after AI-assisted coding sessions to turn changed code and conversation context into learning notes, reusable knowledge cards, progress entries, review prompts, and interview-prep material. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Auto mode can scan project content and read prior conversation or note data. <br>
Mitigation: Confirm the intended project, note directory, and file scope before using Auto mode. <br>
Risk: The skill can create or update many learning-notes files, including calendar, progress, domain index, topic, and card files. <br>
Mitigation: Use version control or backups and review file diffs before accepting changes. <br>
Risk: The skill may run a project-local `scripts/analyze-session.py` helper when depth is automatic. <br>
Mitigation: Allow local script execution only in repositories you trust, or inspect the script before it runs. <br>
Risk: Prompt-history analysis can summarize conversations into persistent learning artifacts. <br>
Mitigation: Use prompt-history analysis only for conversations you are comfortable storing and summarizing. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/lyqqqq66666/vibe-coding-learning) <br>
- [Server-resolved GitHub provenance](https://github.com/lyqqqq66666/vibe-coding-learning/tree/main/skills/vibe-coding-learning) <br>
- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library) <br>
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering) <br>
- [Google Prompt Engineering Guide](https://ai.google.dev/docs/prompt_engineering) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or HTML learning notes, Markdown knowledge cards, calendar and progress Markdown entries, and conversational guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local learning-notes files and may use a project-local analysis script when the selected mode calls for it.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata; skill frontmatter metadata reports 1.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
