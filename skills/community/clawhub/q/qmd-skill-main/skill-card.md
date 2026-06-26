## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pmaeter](https://clawhub.ai/user/pmaeter) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to search, retrieve, and refresh indexed local Markdown notes, documents, and knowledge-base collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and return private notes when broad local folders are added as qmd collections. <br>
Mitigation: Index only Markdown folders intended for agent search and exclude notes that contain secrets or sensitive personal information. <br>
Risk: Installation depends on an external qmd package from GitHub. <br>
Mitigation: Install only after trusting the external package source and reviewing the command before execution. <br>
Risk: Scheduled indexing can keep exposing newly added local Markdown files over time. <br>
Mitigation: Enable scheduled qmd update or embed jobs only for collections that should remain searchable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/pmaeter/qmd-skill-main) <br>
- [qmd Homepage](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce qmd command suggestions and retrieval guidance for local Markdown collections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
