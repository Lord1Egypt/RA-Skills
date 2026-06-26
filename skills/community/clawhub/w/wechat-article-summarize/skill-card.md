## Description: <br>
Reads one or more WeChat public account article links from mp.weixin.qq.com, extracts cleaned text and optional image links, summarizes each article in Chinese with a local summarizer, and saves structured markdown notes or reports to a user-chosen directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JuneLiu1999](https://clawhub.ai/user/JuneLiu1999) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to turn one or more WeChat public account articles into Chinese markdown summaries, single-article notes, or multi-article daily reports for reading, archiving, and follow-up organization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched article text, raw HTML, image links, and summaries may be stored locally in output or work directories. <br>
Mitigation: Choose only directories where retaining full article copies and generated summaries is acceptable, and clean temporary work directories when the material should not be retained. <br>
Risk: The skill relies on a local summarize command and its configured provider to process article content. <br>
Mitigation: Install only when the summarize command and provider configuration are trusted, and verify the summarizer with a small Chinese probe before processing articles. <br>
Risk: Environment files can affect the summarizer configuration and may expose unrelated secrets if untrusted files are used. <br>
Mitigation: Use only trusted env files scoped to the summarizer and avoid environments containing unrelated credentials. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/JuneLiu1999/wechat-article-summarize) <br>
- [Publisher profile](https://clawhub.ai/user/JuneLiu1999) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown files with Chinese summaries, article metadata, mindmap-style sections, and optional image links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes article extraction artifacts, summary JSON, and final markdown reports to user-selected local directories.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
