## Description: <br>
Build a persistent, searchable knowledge base from articles, papers, documents, and notes using BlueColumn. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, and developers use this skill to save selected articles, papers, documents, and notes to BlueColumn, then recall synthesized answers and citations from the stored knowledge base. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a sensitive BlueColumn API key. <br>
Mitigation: Keep the bc_live API key private and avoid logging, sharing, or embedding it in saved content. <br>
Risk: Selected research content is stored in remote persistent memory. <br>
Mitigation: Avoid saving confidential or regulated material unless BlueColumn retention and deletion controls meet the user's requirements. <br>


## Reference(s): <br>
- [BlueColumn API Reference](references/api.md) <br>
- [BlueColumn](https://bluecolumn.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a BlueColumn bc_live API key; saved content and recall results are handled by BlueColumn.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
