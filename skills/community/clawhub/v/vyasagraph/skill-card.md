## Description: <br>
No more agentic amnesia. Gives your agent short-term + long-term memory: hot survivable context + knowledge graph for permanent recall. Semantic search, graph relations, no server required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minopop](https://clawhub.ai/user/minopop) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use VyasaGraph to add local short-term session state and long-term knowledge graph memory to an agent, including semantic recall, relationships, project tracking, and error history across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent local memory can retain sensitive or unnecessary user information if agents record broad categories of facts automatically. <br>
Mitigation: Define what may be remembered before enabling the skill, avoid secrets and sensitive personal data, and regularly review or delete memory.db. <br>
Risk: When OPENAI_API_KEY is configured, stored facts used for embeddings may be sent to OpenAI. <br>
Mitigation: Leave OPENAI_API_KEY unset when stored facts should remain fully local; VyasaGraph can fall back to keyword search. <br>


## Reference(s): <br>
- [VyasaGraph project homepage](https://github.com/minopop/vyasagraph) <br>
- [VyasaGraph npm package](https://www.npmjs.com/package/vyasagraph) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local files for session state and an embedded local database for long-term memory; OpenAI embeddings are optional.] <br>

## Skill Version(s): <br>
1.2.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
