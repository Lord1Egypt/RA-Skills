## Description:

通过 AISA Tavily 抽取接口从 URL 获取干净正文。触发条件：当用户已经有 URL，需要读取页面正文做总结、对比或证据审查时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisadocs](https://clawhub.ai/user/aisadocs)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they already have one or more URLs and need clean page text for summarization, comparison, or evidence review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled client exposes broader API-backed search and AI synthesis actions beyond URL extraction.

Mitigation: Review the available CLI commands before installation and restrict use to environments where those broader AISA_API_KEY-backed requests are acceptable.

Risk: Private URLs or sensitive queries may be sent to external AISA endpoints during extraction or related commands.

Mitigation: Avoid submitting private URLs, confidential content, or sensitive queries unless the publisher documents narrower data handling and command behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aisadocs/skills/tavily-extract-zh)
- [AISA service](https://aisa.one)
- [AISA API endpoint](https://api.aisa.one/apis/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; the CLI returns extracted text or JSON responses from AISA endpoints.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and python3.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
