## Description: <br>
SearXNG Web Search runs queries against a configurable SearXNG meta-search endpoint and returns structured web search results from engines such as Baidu and Bing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiaoshaohua](https://clawhub.ai/user/qiaoshaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to retrieve current public web information, compare search results across engines, and cite source URLs before answering research, news, product, policy, or general information questions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default configuration sends search queries to an unknown public SearXNG server over unencrypted HTTP. <br>
Mitigation: Use a trusted HTTPS or self-hosted SearXNG endpoint before searching private, client, account, health, legal, financial, or workplace-sensitive topics. <br>
Risk: Search results are public web-search output from Baidu and Bing through the configured endpoint and may be incomplete or misleading. <br>
Mitigation: Verify important answers against cited source pages and treat the search output as discovery evidence rather than authoritative fact. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiaoshaohua/youyiai-web-search) <br>
- [Artifact-declared homepage](https://github.com/robydeeptool/hermes-skills) <br>
- [Configured SearXNG endpoint](http://175.24.233.186:8890) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text status output or JSON search results containing title, URL, source engine, and summary fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Result count is capped at 20; the SearXNG endpoint can be overridden with SEARXNG_ENDPOINT or an explicit endpoint argument.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, README version record, and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
