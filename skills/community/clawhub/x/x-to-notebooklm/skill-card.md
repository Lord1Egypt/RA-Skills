## Description: <br>
Parse X (Twitter) articles with r.jina.ai and upload the extracted content to Google NotebookLM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicoxia](https://clawhub.ai/user/nicoxia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to capture public X article content, place it into NotebookLM, and return notebook/source identifiers for follow-up reading and analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted URL, notebook name, or notebook ID values may reach shell commands. <br>
Mitigation: Use only trusted public URLs and simple notebook names or IDs; review the script before running it in an environment with sensitive credentials. <br>
Risk: Fetched page content and uploaded files may contain sensitive or unintended data. <br>
Mitigation: Use the skill only with non-sensitive public content, and assume fetched content is sent to r.jina.ai and Google NotebookLM. <br>
Risk: Temporary uploaded-content files may remain on disk after some execution paths. <br>
Mitigation: Inspect and remove relevant temporary files manually after running the skill until cleanup behavior is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nicoxia/x-to-notebooklm) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nicoxia) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Console text and Markdown-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports article title, original URL, Notebook ID, Source ID, and processing status when execution succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
