## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aryannate](https://clawhub.ai/user/aryannate) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to search local Markdown notes, documentation, and knowledge bases, then retrieve matching files or chunks from indexed collections. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs qmd through a Bun-based GitHub install path and depends on the upstream qmd project. <br>
Mitigation: Install only when the upstream qmd project and install path are trusted. <br>
Risk: Indexed Markdown folders may include secrets or highly sensitive notes that become searchable by the agent. <br>
Mitigation: Add only Markdown folders intended for agent search and exclude secret or highly sensitive collections. <br>
Risk: Scheduled updates or embedding refreshes can continue re-indexing local content in the background. <br>
Mitigation: Enable scheduled updates only when ongoing background re-indexing is desired. <br>


## Reference(s): <br>
- [qmd project homepage](https://github.com/tobi/qmd) <br>
- [ClawHub release page](https://clawhub.ai/aryannate/qmd-skill-4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, text] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON-producing qmd commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides agents to use qmd search by default, retrieve Markdown documents, maintain local indexes, and reserve slower semantic or hybrid search modes for fallback use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
