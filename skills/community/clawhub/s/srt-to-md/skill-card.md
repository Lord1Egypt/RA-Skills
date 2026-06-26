## Description: <br>
Converts SRT subtitle files into structured Markdown documents with transcript cleanup, content analysis, and optional research enrichment. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[syajask](https://clawhub.ai/user/syajask) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn video subtitles from sources such as Bilibili or YouTube into readable Markdown notes, knowledge articles, or research reports. It is suited for public or non-sensitive subtitle files, with the optional research stage skipped for private transcripts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional web search enrichment may expose names, topics, or keywords from private transcripts to search tools. <br>
Mitigation: Use normally for public videos and non-sensitive subtitles; skip the web search stage for private meetings, unpublished material, or transcripts containing personal information. <br>


## Reference(s): <br>
- [Search strategy reference](references/search_strategy.md) <br>
- [Document template](assets/doc_template.md) <br>
- [ClawHub skill listing](https://clawhub.ai/syajask/srt-to-md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown document and UTF-8 subtitle text file, with optional source URLs for research enrichment] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a primary Markdown document and a time-stamped subtitle text file; optional web search may add references.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
