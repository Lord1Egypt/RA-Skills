## Description:

Realtime Web Search lets an agent query Baidu-backed web search and summary routes for changing facts, current news, and cross-source verification with traceable JSON outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch recent public web results, fact-check changing claims, and gather Chinese web evidence through Baidu search routes. It is not intended for private database queries or browser automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Baidu credential may be sent to endpoint override URLs configured in the environment.

Mitigation: Use scoped Baidu credentials and set endpoint override variables only to trusted destinations.

Risk: Search queries and returned source metadata may appear in process output or collected logs.

Mitigation: Avoid sensitive queries and handle command output as potentially logged data.

Risk: The security verdict is suspicious because endpoint destinations are environment-configurable.

Mitigation: Review the installed skill and environment before execution; keep overrides unset unless a trusted destination is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangziiiiii/skills/realtime-web-search)
- [Publisher profile](https://clawhub.ai/user/wangziiiiii)
- [Baidu Qianfan web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search)
- [Baidu Qianfan chat search endpoint](https://qianfan.baidubce.com/v2/ai_search/chat/completions)
- [Baidu Qianfan web summary endpoint](https://qianfan.baidubce.com/v2/ai_search/web_summary)
- [Jisu API](https://jisuapi.com)
- [Jisu EPC](https://jisuepc.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON search results printed to stdout, with errors as text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY; result items may include source, source_endpoint, request_id, answer, title, url, content, date, or provider-specific fields.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
