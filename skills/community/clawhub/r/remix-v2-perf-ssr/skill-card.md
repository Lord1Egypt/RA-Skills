## Description: <br>
Remix v2 performance, streaming, caching, and server/client boundary guidance for configuring HTTP caching, server-only modules, hydration safety, prefetching, and asset preload behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to get Remix v2 SSR performance guidance for streaming deferred data, cache headers, prefetch behavior, hydration-safe rendering, and separating server-only from client-only modules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Applying caching or prefetch recommendations to authenticated or personalized routes without review can expose user-specific content or create unnecessary duplicate requests. <br>
Mitigation: Review cache headers, prefetch modes, and route sensitivity before applying the guidance; use private or no-store policies for personalized data. <br>


## Reference(s): <br>
- [HTTP Caching with the headers Route Export](references/headers-caching.md) <br>
- [Hydration Safety](references/hydration.md) <br>
- [links Export - Preloading and Image Notes](references/links-preload.md) <br>
- [Prefetching with Link and PrefetchPageLinks](references/prefetch.md) <br>
- [Server/Client Split - .server.ts, .client.ts, and Env Vars](references/server-client-split.md) <br>
- [Streaming with defer and Await](references/streaming.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration guidance] <br>
**Output Format:** [Markdown guidance with TypeScript/TSX code examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; no tool calls, commands, or generated files are produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
