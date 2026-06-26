## Description: <br>
Fetches web page content with privacy-first local parsing by default, optional Jina Reader cleanup, noise removal, domain allowlists, and character limits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vimself](https://clawhub.ai/user/vimself) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to fetch readable web page text for downstream agent work while controlling privacy posture, allowed domains, and output length. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote cleanup can send URL and page content through Jina AI. <br>
Mitigation: Use the default local mode for private, internal, tokenized, or sensitive URLs; only enable --remote or DEFAULT_MODE=remote for pages suitable for third-party processing. <br>
Risk: Without an allowlist, the fetch helper can access any requested domain. <br>
Mitigation: Set ALLOWED_DOMAINS or use --allow to restrict fetching to approved domains. <br>
Risk: Fetched pages may produce long or noisy content for the calling agent. <br>
Mitigation: Use MAX_CHARS or --max-chars to cap output and rely on the local cleaner's script, style, navigation, and layout removal. <br>


## Reference(s): <br>
- [Smart Web Fetch Safe ClawHub release](https://clawhub.ai/vimself/smart-web-fetch-safe) <br>
- [Jina Reader remote cleanup endpoint](https://r.jina.ai/http://{url}) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [Plain text or JSON object containing success, url, content, source, mode, and error fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Character-limited output; defaults to 10000 characters and can be capped with MAX_CHARS or --max-chars.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
