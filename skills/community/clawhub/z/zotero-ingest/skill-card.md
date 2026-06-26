## Description: <br>
Add papers (arXiv, DOI, URL) to Zotero via the Zotero REST API for citation management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nissan](https://clawhub.ai/user/nissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research users use this skill to add arXiv papers, DOI-linked papers, URLs, and related metadata to a Zotero library through the Zotero REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents authority to write to a Zotero library and includes helpers that can create collections, move items, and delete items. <br>
Mitigation: Use a narrowly scoped Zotero API key and require explicit user confirmation with item previews before collection administration or deletion actions. <br>
Risk: The skill requires sensitive Zotero credentials. <br>
Mitigation: Store the API key in a credential manager or environment variable and avoid exposing it in prompts, logs, or generated artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/nissan/zotero-ingest) <br>
- [Publisher Profile](https://clawhub.ai/user/nissan) <br>
- [Zotero REST API User Endpoint](https://api.zotero.org/users/10425097) <br>
- [Zotero Collections Endpoint](https://api.zotero.org/users/10425097/collections) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Zotero API key and outbound network access to the Zotero REST API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
