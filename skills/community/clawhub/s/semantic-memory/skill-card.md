## Description: <br>
OpenClaw Agent Chinese long-term memory system using jieba TF-IDF and vector retrieval for Chinese-first hybrid semantic search across multiple agent memory collections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackxc2026](https://clawhub.ai/user/jackxc2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to import Markdown memory files into ChromaDB and retrieve Chinese-language notes with hybrid TF-IDF, vector, and keyword scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported private notes can be exposed if the default ChromaDB service is bound to a network-accessible interface. <br>
Mitigation: Review the memory folder before import and bind ChromaDB to 127.0.0.1 unless authentication and firewall controls are in place. <br>
Risk: Pointing CHROMA_HOST at an untrusted remote server can disclose queries and retrieved memory content. <br>
Mitigation: Use only trusted ChromaDB endpoints for CHROMA_HOST and avoid untrusted remote servers. <br>
Risk: The TF-IDF cache uses pickle files, which can be unsafe if the cache directory is writable by untrusted parties. <br>
Mitigation: Keep the TF-IDF cache directory private and do not reuse cache files from untrusted sources. <br>


## Reference(s): <br>
- [Semantic Memory ClawHub page](https://clawhub.ai/jackxc2026/semantic-memory) <br>
- [ChromaDB](https://www.trychroma.com/) <br>
- [Python](https://www.python.org/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with shell commands and Python usage examples; scripts print plain-text import status and ranked search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes top results with combined score, vector similarity, TF-IDF similarity, source, agent, collection, and document excerpt.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
