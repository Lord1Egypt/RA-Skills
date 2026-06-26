## Description: <br>
Threadline helps developers add persistent, scoped memory to AI agents by injecting relevant user context before model calls and updating stored context after responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vidursharma202-del](https://clawhub.ai/user/vidursharma202-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers building AI agents, chatbots, and assistants use this skill to integrate Threadline memory with OpenAI, Anthropic, Vercel AI SDK, LangChain, or REST API workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, responses, and inferred context may be sent to and stored by a third-party persistent memory service. <br>
Mitigation: Disclose this data flow to users, obtain opt-in consent before using it with real users, and verify retention, export, and deletion controls. <br>
Risk: The skill can store broad user context, including sensitive inferred scopes such as emotional state or relationship information. <br>
Mitigation: Avoid secrets and regulated data, limit enabled scopes to the minimum needed for the agent, and review whether sensitive scopes are appropriate. <br>
Risk: Injected memory becomes part of the enriched system prompt and could expose private user context if logged or displayed. <br>
Mitigation: Do not log or expose enriched system prompts, and review prompt-safety controls before production use. <br>


## Reference(s): <br>
- [Threadline homepage](https://threadline.to) <br>
- [Threadline documentation](https://threadline.to/docs) <br>
- [Threadline API reference](https://api.threadline.to/docs) <br>
- [threadline-sdk npm package](https://www.npmjs.com/package/threadline-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Configuration] <br>
**Output Format:** [Markdown with TypeScript and REST API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires THREADLINE_API_KEY and a stable userId; produces integration guidance rather than standalone files.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
