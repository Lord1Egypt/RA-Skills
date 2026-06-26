## Description: <br>
WeKnora imports documents and supports knowledge retrieval through the WeKnora API for file, URL, Markdown, hybrid search, and knowledge-detail workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lyingbug](https://clawhub.ai/user/lyingbug) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to load documents, URLs, or Markdown into WeKnora knowledge bases and retrieve relevant content through knowledge browsing and hybrid search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may target an untrusted or incorrect WeKnora base URL. <br>
Mitigation: Confirm WEKNORA_BASE_URL points to the user's trusted WeKnora server before making API calls. <br>
Risk: Long-lived API keys can be exposed if stored in shell startup files or shared environments. <br>
Mitigation: Use a least-privilege API key where possible and avoid storing long-lived keys on shared machines. <br>
Risk: Edit, reparse, or delete operations can change shared knowledge-base data. <br>
Mitigation: Require explicit user confirmation of the exact knowledge entry before performing edit, reparse, or delete calls. <br>


## Reference(s): <br>
- [WeKnora ClawHub Skill Page](https://clawhub.ai/lyingbug/weknora) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WEKNORA_BASE_URL and WEKNORA_API_KEY; may propose curl requests that read, write, edit, or delete WeKnora knowledge entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
