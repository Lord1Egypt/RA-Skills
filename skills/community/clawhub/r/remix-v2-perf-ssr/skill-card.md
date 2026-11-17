## Description:

Remix v2 performance, streaming, caching, and server/client boundaries. Use when configuring HTTP caching, server-only modules, hydration safety, or prefetch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Remix v2 SSR performance guidance, including streaming with defer and Await, HTTP caching headers, route prefetching, hydration safety, asset preloading, and server/client module boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: window.ENV examples can expose sensitive values if developers publish raw environment data.

Mitigation: Expose only public values and prefer the serializer pattern called out by the security guidance.

Risk: Caching guidance may cause user-specific HTML or data to be cached if applied to personalized routes without review.

Mitigation: Review proposed Cache-Control and headers export changes before deployment, especially on authenticated or personalized routes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anderskev/skills/remix-v2-perf-ssr)
- [HTTP Caching with the headers Route Export](artifact/references/headers-caching.md)
- [Hydration Safety](artifact/references/hydration.md)
- [links Export - Preloading and Image Notes](artifact/references/links-preload.md)
- [Prefetching with Link and PrefetchPageLinks](artifact/references/prefetch.md)
- [Server/Client Split - .server.ts, .client.ts, and Env Vars](artifact/references/server-client-split.md)
- [Streaming with defer and Await](artifact/references/streaming.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with inline TypeScript, TSX, HTTP header, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no tools, MCP servers, credential environment variables, or runtime execution were detected in release evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
