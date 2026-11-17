## Description:

Search Term Miner analyzes paid advertising search-term exports to harvest converting queries into new keywords or ad groups, propose negative keywords, rank wasted spend with n-grams, and produce a maintenance diff with ROAS spend-efficiency notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and advertising analysts use this skill to mine paid-search term exports for converting queries, negative keywords, waste-heavy n-grams, and recurring campaign maintenance actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles business-sensitive advertising search-term exports and may preserve analysis summaries in memory.

Mitigation: Use exports intended for analysis, avoid including unrelated sensitive data, and confirm before saving reusable summaries or promoting findings to shared memory.

Risk: Keyword additions, moves, and negative-keyword recommendations can harm campaign performance if applied without review.

Mitigation: Review proposed add, negate, and move actions, including thresholds, match types, and measured cost or conversion evidence, before applying them in an ad platform.

Risk: Optional ad-platform API access can expand data exposure beyond manual exports.

Mitigation: Prefer manual exports unless API access is necessary, and enable keyed platform access only with appropriate account authorization and data handling controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/search-term-miner)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown maintenance diff with keyword, negative-keyword, n-gram waste, score, and handoff sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save user-confirmed summaries under memory/ad/search-term-miner/ and promote durable findings to memory hot-cache and open-loops.]

## Skill Version(s):

19.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
