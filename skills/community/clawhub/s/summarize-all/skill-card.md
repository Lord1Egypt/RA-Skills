## Description:

智能总结工具 - 自动检测内容类型、智能选择长度、缓存、关键点提取。支持网页、PDF、图片、音频、YouTube。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gu2003li](https://clawhub.ai/user/gu2003li)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to summarize, compare, translate, search, and analyze web pages, PDFs, images, audio, YouTube links, and plain text through a configurable command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional API server may expose summarization of local files and outbound network requests without authentication.

Mitigation: Run the server only on localhost behind authentication, and restrict access to local paths and internal network destinations.

Risk: Summarized content is sent to the configured model endpoint.

Mitigation: Use only trusted API endpoints and avoid submitting content that violates privacy, confidentiality, or data handling requirements.

Risk: API keys, cache, history, tags, and keyword files are stored as sensitive local data.

Mitigation: Protect the local configuration directory, limit file permissions, and clear stored data when it is no longer needed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text summaries, Q&A answers, comparisons, translations, structured reports, configuration commands, and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured OpenAI-compatible API endpoint; may cache summaries, history, tags, keywords, and configuration locally.]

## Skill Version(s):

3.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
