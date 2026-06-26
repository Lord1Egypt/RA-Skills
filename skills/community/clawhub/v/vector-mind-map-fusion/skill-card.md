## Description: <br>
Vector Mind Map Fusion is a three-layer vector memory system that helps an agent extract, organize, store, and retrieve structured semantic memories across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxiaofeng0811-lgtm](https://clawhub.ai/user/dxiaofeng0811-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain semantic memory across OpenClaw sessions, including capturing important user-provided knowledge, consolidating it into L1/L2/L3 memory layers, and recalling relevant records through vector and keyword search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads OpenClaw session history and stores cross-session semantic memory, which may retain sensitive user content. <br>
Mitigation: Install only where session history processing is expected, review retention and deletion behavior, and avoid use on sessions containing secrets until redaction controls are clear. <br>
Risk: Memory and query text may be sent to the configured embedding service. <br>
Mitigation: Use a trusted local Ollama endpoint by default and avoid remote OLLAMA_BASE_URL values unless the endpoint is explicitly trusted. <br>
Risk: The security summary flags under-disclosed background scanning, credential use, and outbound messaging. <br>
Mitigation: Review credential requirements and disable or audit the Lark/Feishu notification path before installation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dxiaofeng0811-lgtm/vector-mind-map-fusion) <br>
- [README](artifact/README.md) <br>
- [L1 extraction flow](artifact/docs/l1_flow.md) <br>
- [L2 consolidation flow](artifact/docs/l2_flow.md) <br>
- [L3 retrieval flow](artifact/docs/l3_flow.md) <br>
- [Recall API](artifact/docs/recall_api.md) <br>
- [Ollama download](https://ollama.com/download) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, Python command examples, configuration snippets, and JSON-like recall results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory files, query an Ollama embedding service, and return ranked semantic-memory records with scores, tiers, and memory types.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
