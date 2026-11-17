## Description:

Search for current HK tech sector dynamics via public web and generate a structured daily opening brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill before the Hong Kong market opens to create a concise HK technology sector brief from current public web sources. It is not intended for historical analysis, portfolio picks, or non-HK sectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests persistent memory write access even though the release evidence describes a narrow daily market-brief workflow.

Mitigation: Remove memory_write before installation or restrict it to a clearly scoped, user-approved purpose.

Risk: Current market briefs can be incomplete or stale if public web search results are sparse, delayed, or regionally inconsistent.

Mitigation: Review the cited market news before relying on the brief for business decisions and avoid treating it as portfolio advice.

## Reference(s):

- [Sector Opening Note on ClawHub](https://clawhub.ai/terrycarter1985/skills/sector-opening-note)
- [Yahoo Finance Technology Sectors](https://finance.yahoo.com/sectors/technology)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown brief with structured HK technology market sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses current public web search and is scoped to HK market opening notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
