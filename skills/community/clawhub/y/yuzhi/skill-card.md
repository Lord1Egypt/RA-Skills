## Description: <br>
御知库 is a personal knowledge-base skill that stores Markdown, PDF, and text documents locally and helps an agent search them before answering knowledge questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zton100](https://clawhub.ai/user/zton100) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and individual users use this skill to maintain a local personal knowledge base and have an agent add, list, search, and summarize stored documents before answering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Added documents are copied into a persistent local knowledge base and may be used in later answers. <br>
Mitigation: Do not add secrets or highly sensitive documents unless local storage and later retrieval are acceptable. <br>
Risk: PDF ingestion depends on local pdfplumber support and may fail or extract incomplete text. <br>
Mitigation: Verify PDF support in the target environment and review extracted content for important documents. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zton100/yuzhi) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown text with CLI command examples and search-result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a persistent local SQLite database under ~/.yuzhi for indexed document text.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
