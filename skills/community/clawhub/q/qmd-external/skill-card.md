## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, knowledge workers, and agents use this skill to search local Markdown notes, documentation, and indexed knowledge bases, then retrieve matching documents or chunks for follow-up work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can index and search local Markdown files, including sensitive notes if broad directories are indexed. <br>
Mitigation: Index only narrow, intended folders and avoid sensitive notes unless they are meant to be searchable by the agent. <br>
Risk: The optional automatic re-indexing job can continue running in the background. <br>
Mitigation: Enable scheduled re-indexing only when ongoing background updates are desired, and review the configured command and schedule. <br>
Risk: Installation depends on the upstream qmd project and a local qmd binary. <br>
Mitigation: Install only after deciding to trust the upstream qmd project and verify that the required qmd binary is available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/levineam/qmd-external) <br>
- [qmd project homepage](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include qmd search, retrieval, indexing, embedding, and maintenance commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
