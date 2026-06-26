## Description: <br>
Searches the web through a configured SearXNG meta-search instance and returns aggregated results for current facts, news, and other web queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simoncatbot](https://clawhub.ai/user/simoncatbot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to issue web searches, retrieve current information, and configure public or self-hosted SearXNG search access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries may leave the local environment for the configured SearXNG instance and downstream search engines. <br>
Mitigation: Use a controlled and trusted SearXNG instance for sensitive contexts, and do not submit secrets, private customer data, unreleased business information, or sensitive personal queries. <br>
Risk: Public SearXNG instances may rate-limit, block automated access, or return unavailable service errors. <br>
Mitigation: Configure rate limiting, verify the selected instance before use, and self-host SearXNG for heavier or reliability-sensitive usage. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/simoncatbot/web-search-searxng) <br>
- [SearXNG Public Instances](https://searx.space/) <br>
- [Default SearXNG Configuration](https://raw.githubusercontent.com/searxng/searxng/master/searx/settings.yml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON search results, with Markdown setup guidance and shell commands in documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output includes result titles, URLs, excerpts, source engines, suggestions when available, and optional category, engine, time range, and result limit controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
