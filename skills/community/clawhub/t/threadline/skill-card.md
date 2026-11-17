## Description:

Threadline helps AI agent developers add persistent user memory and scoped context injection across OpenAI, Anthropic, Vercel AI SDK, LangChain, and REST integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vidursharma202-del](https://clawhub.ai/user/vidursharma202-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when building AI agents, chatbots, or assistants that need persistent per-user context across sessions. It provides guidance and examples for calling Threadline before and after model interactions while controlling memory scopes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation content may be stored in a third-party persistent memory service.

Mitigation: Use the skill only after explicit user opt-in, redact secrets and regulated data before update(), and avoid sending full raw conversations when narrower fields are sufficient.

Risk: Retrieved memory may be treated as high-priority model context.

Mitigation: Keep retrieved memory outside the system prompt where possible, or clearly mark it as untrusted context before the model uses it.

Risk: Production integrations depend on an external SDK and API key.

Mitigation: Pin and review the SDK version, protect THREADLINE_API_KEY, and review examples before deployment.

## Reference(s):

- [Threadline homepage](https://threadline.to)
- [Threadline documentation](https://threadline.to/docs)
- [Threadline API reference](https://api.threadline.to/docs)
- [threadline-sdk on npm](https://www.npmjs.com/package/threadline-sdk)
- [ClawHub skill page](https://clawhub.ai/vidursharma202-del/skills/threadline)
- [ClawHub publisher profile](https://clawhub.ai/user/vidursharma202-del)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires THREADLINE_API_KEY for the described integrations.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
