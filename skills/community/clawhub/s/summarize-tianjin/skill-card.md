## Description: <br>
Summarize URLs or files with the summarize CLI (web, PDFs, images, audio, YouTube). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tianjin-ren](https://clawhub.ai/user/tianjin-ren) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize web pages, local files, images, audio, and YouTube links through the summarize CLI, with configurable model provider, extraction, and output options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Content submitted for summarization may be sent to selected third-party AI model providers or extraction services. <br>
Mitigation: Avoid sensitive, private, regulated, or copyrighted content unless provider policies and configured fallback services have been reviewed. <br>
Risk: Optional Firecrawl and Apify fallback behavior can send URLs or YouTube inputs to additional extraction providers. <br>
Mitigation: Configure fallback behavior intentionally and disable optional services when third-party extraction is not appropriate. <br>


## Reference(s): <br>
- [Summarize homepage](https://summarize.sh) <br>
- [ClawHub skill page](https://clawhub.ai/tianjin-ren/summarize-tianjin) <br>
- [Publisher profile](https://clawhub.ai/user/tianjin-ren) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples; CLI output may be plain text or JSON depending on flags.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summary length and maximum output tokens can be configured with CLI flags.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
