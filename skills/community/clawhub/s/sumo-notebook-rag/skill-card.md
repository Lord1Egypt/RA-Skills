## Description: <br>
Searches the SumoNoteBook knowledge base and returns previews of the top three relevant text entries for agent context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sumo0221](https://clawhub.ai/user/sumo0221) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query a local SumoNoteBook markdown knowledge base and add relevant notebook excerpts to the current task context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local notebook indexing may make sensitive notes available in future agent context. <br>
Mitigation: Avoid indexing secrets or regulated data, and review indexed content before using the skill with sensitive notes. <br>
Risk: The skill depends on local query and ingestion scripts plus local Ollama and LanceDB services. <br>
Mitigation: Inspect the referenced local scripts and confirm the local Ollama and LanceDB setup is trusted before use. <br>


## Reference(s): <br>
- [Sumo Notebook RAG on ClawHub](https://clawhub.ai/sumo0221/sumo-notebook-rag) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown-like text with query echo, ranked results, filenames, relevance scores, and content previews.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the top three results with approximately 300-character previews; depends on local Ollama and LanceDB setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
