## Description:

Search and fetch real K12 primary, middle, and high school questions from Tizhuang by subject, grade, textbook edition, question type, difficulty, year, chapter, or knowledge point, and create practice pages, quizzes, answer-checking flows, and paper-builder handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weishao2](https://clawhub.ai/user/weishao2)

### License/Terms of Use:

MIT-0

## Use Case:

External educators, learners, and agent users use this skill to retrieve authentic K12 questions, generate answer-hidden practice pages or quizzes, check answers, and hand structured paper-building requests to Tizhuang.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials could be sent to an unintended service if QUESTION_SERVICE_URL is configured to an untrusted endpoint.

Mitigation: Use the default trusted service URL or a clearly trusted HTTPS endpoint, avoid setting QUESTION_SERVICE_URL in shared or untrusted environments, and keep QUESTION_SERVICE_LICENSE and QUESTION_SERVICE_ACCOUNT_TOKEN local.

Risk: Public share links can expose selected paper content to anyone with the URL, including answers or no-watermark views when explicitly enabled.

Mitigation: Use questions-only watermarked shares by default, enable answer-including or no-watermark options only for intentional disclosure, and rotate or revoke only after matching exact share records.

Risk: Question content may include legacy HTML when embedded outside the hosted practice page.

Mitigation: Treat raw HTML as untrusted and sanitize it in any client that embeds returned question content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weishao2/skills/tizhuang-question-bank)
- [Server-Resolved GitHub Source](https://github.com/weishao2/tizhuang-agent-skills/tree/main/skills/question-bank)
- [API Reference](references/api.md)
- [Default Tizhuang API Endpoint](https://tizhuang.qcscience.cc/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline shell commands, service URLs, and question-bank results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include temporary practice page URLs, paper-builder handoff URLs, or public share URLs; credentials must remain local and out of chat.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
