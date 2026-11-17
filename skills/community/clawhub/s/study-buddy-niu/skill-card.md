## Description:

Study Buddy helps learners prepare for Japanese N2/N1 and software architect exams with quiz generation, automatic grading, wrong-answer review, progress tracking, and study-plan guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[it-worker-club](https://clawhub.ai/user/it-worker-club)

### License/Terms of Use:

MIT-0

## Use Case:

External learners and self-study users can use this skill to practice exam questions, receive answer explanations, review mistakes, and generate daily study plans. It is designed around Feishu/OpenClaw workflows and a Feishu Bitable question base.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Feishu Bitable question base and associates study activity with user IDs.

Mitigation: Install only with user awareness of that data flow, add consent and deletion controls, and avoid logging raw answers or unnecessary identifiers.

Risk: Broad trigger phrases and answer detection can misclassify short user messages as quiz answers or study commands.

Mitigation: Narrow trigger phrases for production use and require an active answer session before grading short answer inputs.

Risk: Raw error messages can expose implementation or service details to end users.

Mitigation: Replace raw error text with generic user-facing messages while retaining sanitized operational logs.

Risk: In-memory answer and question caches can grow without explicit bounds.

Mitigation: Add cache limits and session expiration so abandoned study sessions are cleaned up automatically.

Risk: Generated practice value depends on the quality and accuracy of the external question bank.

Mitigation: Review imported questions, keep source metadata, and periodically audit explanations and correct answers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/it-worker-club/skills/study-buddy-niu)
- [Feishu Bitable question base](https://my.feishu.cn/base/SoZ5bkTBOa3LQisZHO1cAQuknDh)
- [Feishu Bitable configuration document](https://my.feishu.cn/docx/TC9adYy1uo3iGsxIorpcB6denHe)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-formatted chat text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns quizzes, answer feedback, progress summaries, wrong-answer summaries, and study-plan guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
