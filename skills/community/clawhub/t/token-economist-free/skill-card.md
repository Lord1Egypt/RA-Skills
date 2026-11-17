## Description: <br>
Token Economist Free helps an agent reduce token use in long conversations by summarizing older context, reusing similar prior answers, and preserving protected content such as code, errors, and key decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill during long conversations or repeated questions to reduce token consumption through context compression, semantic caching, and adaptive optimization. It is most relevant when older conversation history is useful but can be summarized without losing protected content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summarizing older conversation context can omit nuance that may matter later in the session. <br>
Mitigation: Use quality-first mode or disable optimization for precision-critical work, and review summaries before relying on them for important decisions. <br>
Risk: Session-level caching can reuse a prior answer when the current request is only superficially similar. <br>
Mitigation: Clear the cache or raise matching strictness for sensitive or changing topics, and verify cached responses before acting on them. <br>
Risk: Sensitive session content may be included in summaries or cached responses. <br>
Mitigation: Avoid using the skill for highly sensitive sessions unless session-level summarization and caching are acceptable, and use the documented clear-cache or disable commands when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/token-economist-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with status summaries, configuration examples, and natural-language or slash-command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize session context and reuse session-level cached answers; users can clear the cache or disable optimization when needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
