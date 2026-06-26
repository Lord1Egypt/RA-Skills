## Description: <br>
Web search using DuckDuckGo Instant Answer API (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hahahxx](https://clawhub.ai/user/hahahxx) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users, developers, and agents use this skill to run quick public lookups for definitions, calculations, conversions, facts, abstracts, and related topics without external API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to DuckDuckGo over the internet. <br>
Mitigation: Do not submit secrets, credentials, private personal data, customer data, or internal project details in search queries. <br>
Risk: Instant-answer results can be incomplete, stale, or unavailable for some query types. <br>
Mitigation: Use the provided full-search link or authoritative sources to verify critical, current, or high-impact information. <br>
Risk: Fallback parsing without jq can produce character encoding issues in some abstracts. <br>
Mitigation: Install jq when cleaner JSON parsing and text handling are required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hahahxx/web-search-instant) <br>
- [DuckDuckGo Instant Answer API documentation](https://duckduckgo.com/api) <br>
- [README.md](artifact/README.md) <br>
- [CHANGELOG-v1.1.0.md](artifact/CHANGELOG-v1.1.0.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Terminal text by default, with optional plain text or Markdown output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns direct answers, abstracts, definitions, related topics, and a full DuckDuckGo search URL; optional jq improves JSON parsing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and CHANGELOG-v1.1.0.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
