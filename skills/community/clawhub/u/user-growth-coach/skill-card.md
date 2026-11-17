## Description:

A Chinese-language reflection and quick-capture skill that connects current inputs, review history, and daily context to identify behavioral patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal growth coach for quick captures, daily or periodic reviews, commitment tracking, and pattern-focused reflection. It can also generate daily digests from OpenClaw session history when the user enables that workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can broadly read OpenClaw conversation history for daily context and behavioral analysis.

Mitigation: Restrict the sessions directory to intended transcripts, avoid deep mode or cron ingestion for unrelated sessions, and review generated daily digests before reuse.

Risk: Reflection records, captures, commitments, emotions, and daily digests may retain sensitive personal context.

Mitigation: Store memory files in a controlled location, define retention and deletion rules, and avoid recording highly sensitive personal, legal, medical, or financial details.

Risk: Behavior-pattern and psychology-style explanations can be overconfident or misleading.

Mitigation: Treat outputs as reflection prompts rather than medical, mental health, legal, financial, or professional advice, and verify important decisions independently.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jack-yang-ai/skills/user-growth-coach)
- [README](artifact/README.md)
- [Templates](artifact/references/templates.md)
- [Reminders](artifact/references/reminders.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chinese-language text or Markdown responses, JSONL reflection records, and optional Markdown daily digests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local OpenClaw session transcripts and write user-growth memory records or daily digest files when the optional deep review and cron workflows are enabled.]

## Skill Version(s):

2.3.1 (source: server release metadata; artifact frontmatter reports 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
