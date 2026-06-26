## Description: <br>
Local search/indexing CLI (BM25 + vectors + rerank) with MCP mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sambiner](https://clawhub.ai/user/sambiner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to have an agent index local directories with qmd and run BM25, vector, hybrid, or document retrieval commands over local files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Indexed private files can remain searchable in the local qmd cache. <br>
Mitigation: Index only directories intended for local search and treat ~/.cache/qmd as sensitive when it contains private notes, work documents, source code, or other confidential files. <br>
Risk: The skill depends on installing and running the third-party qmd CLI package. <br>
Mitigation: Install only if the upstream qmd package and publisher are trusted in the deployment environment. <br>


## Reference(s): <br>
- [qmd GitHub repository](https://github.com/tobi/qmd) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the qmd CLI; vector and hybrid search depend on Ollama through OLLAMA_URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
