## Description: <br>
Extracts full content from X/Twitter tweets, X Articles, and external pages shared through t.co links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuxiaoyang2007-prog](https://clawhub.ai/user/yuxiaoyang2007-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn X/Twitter links into structured content for analysis, summarization, or downstream content-library workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an xreach/X login session to retrieve X content. <br>
Mitigation: Use a dedicated or low-privilege X account for sensitive workflows and confirm that account access is appropriate before running extraction. <br>
Risk: When FIRECRAWL_API_KEY is configured, external t.co targets can be sent to Firecrawl for page extraction. <br>
Mitigation: Review target links before extraction and only configure Firecrawl when sending external page URLs to that service is acceptable. <br>
Risk: Using --ingest can save extracted content into a content factory. <br>
Mitigation: Use --ingest only when persistent storage is intended and review the extracted content before relying on it downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuxiaoyang2007-prog/x-article-extract) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON or human-readable CLI text; external page content may include markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes extracted title, author, description, content type, engagement metrics, word count, language, and publish date when available.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
