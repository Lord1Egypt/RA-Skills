## Description: <br>
A free webpage content fetching skill that helps agents retrieve Markdown-formatted page content through fallback public services when ordinary fetching is filtered. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to fetch single public webpages as Markdown when normal page retrieval fails or when a Cloudflare-protected page needs an alternate fetch path. It is intended for authorized public pages and does not support authenticated pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary rates the skill suspicious because it is under-scoped and encourages third-party services for crawler-filtered or Cloudflare-protected pages. <br>
Mitigation: Review each request before execution and restrict use to public pages the user is authorized to fetch. <br>
Risk: URLs may contain internal hostnames, authenticated resources, tokens, or sensitive query parameters that would be sent to public fetch services. <br>
Mitigation: Do not submit internal links, authenticated URLs, private documents, or URLs containing credentials, tokens, or sensitive query strings. <br>
Risk: Fetched Markdown can be incomplete, include navigation or advertising content, or omit dynamic page content. <br>
Mitigation: Validate fetched output against the original page context before using it for analysis, publication, or downstream automation. <br>
Risk: The artifact depends on public services and command-line network access, which can fail or be rate-limited. <br>
Mitigation: Handle failed fetches explicitly, add request spacing for repeated use, and avoid treating service output as guaranteed availability. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-content-fetcher-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [r.jina.ai fetch service](https://r.jina.ai/) <br>
- [markdown.new fetch service](https://markdown.new/) <br>
- [defuddle.md fetch service](https://defuddle.md/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown content and command-line examples, with JSON-like status output described by the artifact] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Single-URL fetching; depends on public third-party fetch services and network availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
