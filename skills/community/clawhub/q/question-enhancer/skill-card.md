## Description:

提问质量优化师 - 自动分析、重写、扩展用户问题，并给出完整解答

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to turn Chinese-language questions into clearer, more complete prompts before receiving a structured answer. It diagnoses ambiguity, rewrites the question, adds related follow-up questions, and summarizes the core issue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly redirects every question into a question-improvement workflow without a clear opt-out.

Mitigation: Install only when this behavior is intended, or narrow the trigger and add an explicit opt-out before deployment.

Risk: Users who want direct answers or language flexibility may receive unnecessary prompt rewriting first.

Mitigation: Document the expected Chinese rewrite-and-answer behavior for users and route direct-answer workflows around this skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown text, typically in Chinese, with diagnosis, rewritten question, expanded questions, answer, and summary sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution, file access, tools, or external APIs are described by the skill evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence; skill frontmatter says 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
