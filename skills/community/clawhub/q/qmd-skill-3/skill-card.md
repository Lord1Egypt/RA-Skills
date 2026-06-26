## Description: <br>
Local hybrid search for markdown notes and docs. Use when searching notes, finding related content, or retrieving documents from indexed collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lelo78](https://clawhub.ai/user/Lelo78) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agents, and note-heavy users use this skill to search local Markdown collections, retrieve matching documents, and maintain qmd indexes for keyword, semantic, or hybrid search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed Markdown folders can expose sensitive notes or secrets through agent search and retrieval. <br>
Mitigation: Add only Markdown folders you are comfortable letting the agent search, and avoid indexing secrets or sensitive personal notes. <br>
Risk: The install path depends on the third-party qmd upstream project. <br>
Mitigation: Install only after reviewing and trusting the qmd upstream project and the global Bun install command. <br>
Risk: Scheduled updates can keep background indexing active after setup. <br>
Mitigation: Enable cron or scheduler updates only when ongoing background re-indexing is intended. <br>


## Reference(s): <br>
- [qmd upstream project](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search commands may return file paths, snippets, full Markdown documents, or JSON when --json is requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
