## Description:

Web Search Instant retrieves DuckDuckGo instant answers, definitions, abstracts, calculations, conversions, and related topics without requiring external API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hahahxx](https://clawhub.ai/user/hahahxx)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users can use this skill to retrieve DuckDuckGo instant answers, definitions, abstracts, calculations, conversions, and related topics without external API credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries are sent to DuckDuckGo.

Mitigation: Do not use the skill for secrets, private internal text, or sensitive personal data.

Risk: The artifact documents a global npm command for installing jq.

Mitigation: Prefer installing jq through a trusted operating system package manager.

Risk: DuckDuckGo Instant Answer results may be incomplete, stale, or unavailable for some query types.

Mitigation: Use the returned DuckDuckGo search URL or another source to verify important, recent, or high-impact information.

## Reference(s):

- [DuckDuckGo Instant Answer API](https://duckduckgo.com/api)
- [ClawHub Skill Page](https://clawhub.ai/hahahxx/skills/web-search-instant)
- [README.md](artifact/README.md)
- [TEST-SUMMARY.md](artifact/TEST-SUMMARY.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text, plain text, or Markdown with links and section headers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may include direct answers, abstracts, definitions, related topics, source URLs, and a fallback DuckDuckGo search URL.]

## Skill Version(s):

1.1.0 (source: server release metadata and CHANGELOG-v1.1.0.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
