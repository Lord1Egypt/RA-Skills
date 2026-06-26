## Description: <br>
Read Twitter/X content (single tweet, thread, or user profile) from a URL via TwitterAPI.io when a Twitter/X URL appears in conversation and content is needed without browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and agents use this skill to retrieve Twitter/X tweet, thread, or profile content as clean Markdown for summarization, analysis, indexing, or RAG workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports disagreement between metadata, instructions, services, credentials, and the local script users would run. <br>
Mitigation: Review the skill and referenced local tweet-ingest.py script before installing or running it, and confirm the expected services and credentials. <br>
Risk: Twitter/X targets may be sent to Jina AI or Apify, and thread or profile modes may use Apify credentials and credits. <br>
Mitigation: Use the skill only when that data sharing and Apify usage are acceptable, and verify APIFY_API_KEY use and cost exposure before thread or profile runs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissan/tweet-ingest) <br>
- [Publisher Profile](https://clawhub.ai/user/nissan) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns clean Markdown to stdout; error states are also formatted as Markdown.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
