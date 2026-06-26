## Description: <br>
Uses Scrapling and html2text to fetch readable content from modern web pages, clean WeChat article noise, reduce unnecessary output, and return Markdown or JSON for article, blog, news, and announcement extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jllyzzd2023](https://clawhub.ai/user/jllyzzd2023) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to fetch web page body content, convert pages into Markdown, clean WeChat article boilerplate, and gather readable content for summarization, translation, archiving, or analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches arbitrary user-supplied URLs and returns web content that may be incomplete, misleading, or hostile. <br>
Mitigation: Treat fetched content as untrusted text and review it before using it for decisions, summaries, code, or follow-on actions. <br>
Risk: Batch and selector override options can read local files specified by the user. <br>
Mitigation: Run the skill in a controlled Python environment and provide only intended batch URL lists or selector override files. <br>
Risk: Dependency behavior may change over time because the skill relies on Scrapling and html2text. <br>
Mitigation: Pin dependencies where repeatability is required and review dependency updates before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jllyzzd2023/scrapling-web-fetch) <br>
- [Usage](artifact/references/usage.md) <br>
- [Selector Strategy](artifact/references/selectors.md) <br>
- [Site Overrides Example](artifact/references/site-overrides.example.json) <br>
- [Release 1.0.1 Notes](artifact/references/release-1.0.1.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown by default, with optional JSON records for structured or batch fetches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output is truncated by the max_chars argument and may include selector, title, quality score, final URL, and WeChat cleanup indicators in JSON mode.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
