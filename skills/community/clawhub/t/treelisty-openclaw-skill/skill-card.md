## Description: <br>
Hierarchical project decomposition and planning for breaking down complex projects, structuring information, planning multi-step workflows, or organizing nested hierarchies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Prairie2Cloud](https://clawhub.ai/user/Prairie2Cloud) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers, planners, and agent users use TreeListy to turn topics, outlines, and project goals into structured trees for planning, analysis, and documentation. It supports local pattern-based decomposition, validation, export, and optional display in a trusted TreeListy instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trees may contain secrets, regulated data, or third-party personal details if users include them in planning inputs. <br>
Mitigation: Avoid putting sensitive or personal data into trees unless there is permission and a retention plan. <br>
Risk: The optional push command can send tree content to a WebSocket destination chosen by the user. <br>
Mitigation: Use push only with a trusted local TreeListy bridge; do not pass a token or use a remote host unless the endpoint and network are trusted. <br>
Risk: The release is a Node-based local CLI with a ws dependency. <br>
Mitigation: Install only in environments where using the Node CLI and its dependency is acceptable. <br>


## Reference(s): <br>
- [TreeListy Pattern Reference](references/PATTERNS.md) <br>
- [TreeListy Web App](https://treelisty.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/Prairie2Cloud/treelisty-openclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON, Markdown, Mermaid, CSV, checklist, HTML, and CLI text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local pattern transformations; optional push can send a tree to a trusted TreeListy bridge.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
