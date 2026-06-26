## Description: <br>
Automatically inject relevant skills and protocols into agent context using local embeddings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thekhemistai](https://clawhub.ai/user/thekhemistai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this plugin to automatically find and inject relevant local skill, protocol, and tool documentation into OpenClaw agent runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A remote Ollama endpoint receives prompt text and indexed documentation, including any secrets or sensitive data stored in those documents. <br>
Mitigation: Keep ollamaBaseUrl on localhost, 127.0.0.1, or ::1 unless the remote server is explicitly trusted, and do not index secrets, API keys, or confidential instructions. <br>
Risk: The README install command does not match the reviewed package.json package name. <br>
Mitigation: Verify the package name before installing from npm. <br>
Risk: Low relevance thresholds or broad document indexes can inject irrelevant or misleading context into an agent run. <br>
Mitigation: Tune minScore with debug logs, use pinnedDocs only for trusted high-priority documents, and keep maxResults and maxDocLines bounded. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thekhemistai/skill-preflight) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Ollama nomic-embed-text model](https://ollama.com/library/nomic-embed-text) <br>
- [Ollama](https://ollama.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown context snippets and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Injects relevant local documents according to configured directories, score thresholds, pinned documents, and line limits.] <br>

## Skill Version(s): <br>
1.0.5 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
