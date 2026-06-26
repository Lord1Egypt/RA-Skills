## Description: <br>
Rumour Buster helps an agent check claims and URLs by combining Chinese and English search results, cross-checking findings, scoring credibility, and tracing likely source paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harry720320](https://clawhub.ai/user/harry720320) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent to verify suspicious messages or webpages, compare multilingual search evidence, and produce a structured fact-checking report with source tracing and confidence scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill embeds and handles API credentials in risky, under-disclosed ways. <br>
Mitigation: Ignore the embedded default Tavily key, use your own credential only if you accept plaintext local storage, and delete ~/.rumour-buster-config when it is no longer needed. <br>
Risk: Verification prompts may include sensitive messages, private URLs, or secrets that could be sent to search providers. <br>
Mitigation: Do not paste sensitive content into verification prompts; redact private details before using the skill. <br>
Risk: Fact-checking reports can still be incomplete or misleading if search results are sparse, biased, outdated, or unavailable. <br>
Mitigation: Treat the report as decision support and review the cited sources and confidence score before acting on conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harry720320/rumour-buster) <br>
- [Tavily](https://tavily.com/) <br>
- [Artifact README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown verification reports with setup prompts, search summaries, source tracing, credibility scoring, and final recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Setup may write a local ~/.rumour-buster-config file and may use Tavily or multi-search-engine results when configured.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
