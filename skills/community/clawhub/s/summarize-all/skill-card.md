## Description: <br>
智能总结工具 - 自动检测内容类型、智能选择长度、缓存、关键点提取。支持网页、PDF、图片、音频、YouTube。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gu2003li](https://clawhub.ai/user/gu2003li) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to summarize, compare, translate, and analyze web pages, PDFs, images, audio, YouTube content, and plain text through a CLI or optional API server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarized content is sent to the user's configured AI provider and summaries are stored locally. <br>
Mitigation: Use only trusted endpoints and avoid summarizing sensitive content unless the provider and local storage meet the user's privacy requirements. <br>
Risk: The optional API server can expose unauthenticated summarization access. <br>
Mitigation: Do not run server mode on shared or untrusted networks unless access controls are added and the service is bound locally. <br>
Risk: Webhook forwarding can send summary results to arbitrary destinations. <br>
Mitigation: Restrict or disable webhook forwarding unless destination URLs are trusted and controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gu2003li/summarize-all) <br>
- [Publisher profile](https://clawhub.ai/user/gu2003li) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text; optional API server responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include detected content type, tags, history entries, cached results, comparisons, translations, structured reports, and keyword notifications.] <br>

## Skill Version(s): <br>
3.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
