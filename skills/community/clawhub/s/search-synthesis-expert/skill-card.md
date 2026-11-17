## Description:

Uses sequential-thinking to decompose tasks and formulate search strategies, browser automation (Playwright) for multi-source information search and collection, and final review of synthesized results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-focused agents use this skill to plan, collect, and synthesize multi-source web research for deep research, competitive analysis, technical investigation, and fact-checking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send user-provided search terms or page requests to external websites during browser-based research.

Mitigation: Do not provide passwords, secrets, private customer data, or sensitive internal project names unless external disclosure through searches and page requests is acceptable.

Risk: Locale-sensitive research can return results that do not match the user's intended region or language.

Mitigation: Specify the preferred region and language before collection begins.

Risk: Web research can be incomplete, outdated, or inconsistent across sources.

Mitigation: Use multi-source verification, record source URLs, note information dates, and clearly mark gaps or contradictions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/search-synthesis-expert)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with search strategy, source summaries, synthesized conclusions, and notes on limitations or gaps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Source URLs, credibility notes, timeliness notes, and uncovered aspects may be included when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
