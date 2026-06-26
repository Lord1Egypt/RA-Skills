## Description: <br>
Connect to and search the web using SearXNG (privacy-focused meta search engine). No API keys needed - all searches go through your self-hosted SearXNG instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rdeangel](https://clawhub.ai/user/rdeangel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to search web, news, image, science, file, video, music, social media, and IT results through a configured SearXNG instance. It supports time filters, language settings, safe search, local result caching, rate limiting, and optional full-page content retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to the configured SearXNG instance. <br>
Mitigation: Use a trusted SearXNG instance and avoid searching secrets, internal identifiers, or other sensitive content on untrusted instances. <br>
Risk: The --full-content option makes direct requests to result websites. <br>
Mitigation: Enable full-content retrieval only when those outbound requests and the resulting page content collection are acceptable. <br>
Risk: Local caching can retain sensitive search results for the configured cache period. <br>
Mitigation: Disable caching with --no-cache for sensitive searches or periodically clear the local cache. <br>
Risk: Unsafe shell interpolation of user queries could allow command injection. <br>
Mitigation: Pass query text and options as an argv list, or properly shell-escape query strings when only shell-string execution is available. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rdeangel/searxng-connect) <br>
- [Publisher profile](https://clawhub.ai/user/rdeangel) <br>
- [uv documentation](https://docs.astral.sh/uv/) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results with metadata and error responses; Markdown guidance with inline shell commands in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include title, URL, snippet, image URL, engine, score, and optional fetched page text; local cache entries expire after the configured interval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill-config.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
