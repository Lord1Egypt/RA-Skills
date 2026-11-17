## Description:

Generates structured learning notes from AI coding sessions, including code explanations, knowledge point cards, review prompts, and progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lyqqqq66666](https://clawhub.ai/user/lyqqqq66666)

### License/Terms of Use:

MIT-0

## Use Case:

CS students and developers use this skill after AI-assisted coding sessions to turn code changes and conversation context into learning notes, code explanations, reusable knowledge cards, learning calendars, and progress reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read broad project code, prior learning notes, and selected conversation history.

Mitigation: Ask the agent to list the files and conversation excerpts it intends to inspect before running the skill on confidential projects.

Risk: The skill can write persistent learning artifacts under learning-notes/.

Mitigation: Run it in a workspace where note creation is expected, and review generated files before committing or sharing them.

Risk: The artifact references local Python scripts for session analysis and structure validation.

Mitigation: Do not allow those scripts to run unless their paths and behavior are known and approved in the local workspace.

Risk: Deep mode may use WebSearch for learning resources.

Mitigation: Avoid or disable deep-mode web search for confidential codebases or private project details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lyqqqq66666/skills/vibe-coding-learning)
- [Server-resolved GitHub provenance](https://github.com/lyqqqq66666/vibe-coding-learning/tree/main/skills/vibe-coding-learning)
- [Anthropic Prompt Library](https://docs.anthropic.com/en/prompt-library)
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google Prompt Engineering Guide](https://ai.google.dev/docs/prompt_engineering)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or HTML learning notes, Markdown knowledge cards, calendar entries, progress summaries, and conversational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist generated learning artifacts under learning-notes/ when the agent has filesystem access.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter metadata lists 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
