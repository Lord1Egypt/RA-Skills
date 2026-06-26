## Description: <br>
Publishes Sanity CMS drafts, documents, image assets, and schema-matched content through the Sanity Content API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[squidpunch](https://clawhub.ai/user/squidpunch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content engineers use this skill to prepare Sanity-formatted documents, inspect schemas, upload optional image assets, and create draft CMS records through the Sanity Content API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated Sanity mutations can change CMS data, including production content if live publication is enabled. <br>
Mitigation: Review before installing or running, use a least-privilege Sanity token, prefer a staging dataset, and keep draft mode enabled unless live publication is explicitly intended. <br>
Risk: Incorrect project, dataset, document type, document ID, or asset selection can publish content to the wrong CMS target. <br>
Mitigation: Confirm the project, dataset, document type, document ID, and asset upload before each run. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/squidpunch/sanity-cms) <br>
- [Sanity Content API Reference](references/api.md) <br>
- [Portable Text Reference](references/portable-text.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON document examples and bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create Sanity-formatted JSON documents and invoke a shell script that uploads image assets or mutates CMS documents.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
