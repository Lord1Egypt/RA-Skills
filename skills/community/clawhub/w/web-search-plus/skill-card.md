## Description: <br>
Unified multi-provider web search and URL extraction skill with intelligent routing across search, research, citation, semantic, extraction, and self-hosted providers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robbyczgw-cla](https://clawhub.ai/user/robbyczgw-cla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run web searches, extract URL content, compare providers, and generate grounded research results from configured third-party or self-hosted search services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and extraction URLs are sent to the selected third-party provider. <br>
Mitigation: Use an explicit provider for sensitive work, prefer self-hosted SearXNG when appropriate, and avoid submitting confidential queries or private URLs. <br>
Risk: Search results, queries, and provider failure history may be cached locally. <br>
Mitigation: Use per-call no-cache behavior, disable caching with WSP_DISABLE_CACHE, clear the cache when needed, and keep the cache directory restricted. <br>
Risk: Provider API keys are sensitive credentials. <br>
Mitigation: Prefer environment variables or locked-down configuration files on shared machines, and avoid publishing local credential files. <br>
Risk: URL extraction can expose private or internal targets if private URL safeguards are bypassed. <br>
Mitigation: Keep private URL extraction disabled by default and only opt out for trusted private networks. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robbyczgw-cla/web-search-plus) <br>
- [README](artifact/README.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search and extraction results, with Markdown usage guidance and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can include routing metadata, quality reports, extracted page content, provider diagnostics, and cache controls.] <br>

## Skill Version(s): <br>
3.2.0 (source: frontmatter, changelog, server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
