## Description: <br>
Scrapling Fetch retrieves public webpage content with Scrapling or Jina Reader and returns extracted article text as JSON or plain text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imgolye](https://clawhub.ai/user/imgolye) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to fetch article content from public webpages, including pages where a normal lightweight fetch may fail. It is intended for authorized scraping workflows that need JSON, Markdown-like content, or plain text output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to bypass site protections while scraping webpages. <br>
Mitigation: Use it only for authorized access to public pages, respect site terms and rate limits, and avoid private or token-bearing URLs. <br>
Risk: Fast mode forwards requested URLs to a third-party reader service. <br>
Mitigation: Do not use fast mode for private, internal, sensitive, or untrusted URLs. <br>
Risk: The paid script can charge a billing account and the security evidence flags a hardcoded API key and crafted-URL code execution bug. <br>
Mitigation: Avoid the paid script until the key is removed, charges require explicit confirmation, and URL handling is fixed. <br>


## Reference(s): <br>
- [Supported anti-bot sites](references/antibot-sites.md) <br>
- [Skill metadata](references/skill.json) <br>
- [Scrapling GitHub](https://github.com/D4Vinci/Scrapling) <br>
- [Jina Reader](https://jina.ai/reader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON by default, or plain text when requested; fetched content may include Markdown-style article text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The fetch scripts support a maximum character limit, defaulting to 50000 characters.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
