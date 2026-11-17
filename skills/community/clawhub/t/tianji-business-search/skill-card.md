## Description:

天机商查(Tianji Business Search) helps agents gather public business intelligence about companies, including registration details, shareholder structure, operating status, legal and judicial risk, news, financing, listing status, qualifications, certifications, intellectual property, bids, and public opinion signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiandaox](https://clawhub.ai/user/tiandaox)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill for business due diligence, competitor analysis, market research, and background checks for commercial cooperation. It is intended to organize public company information for reference, with important claims verified against official registries and authoritative sources before decisions are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reports may omit source links or collection dates, making public company claims harder to verify.

Mitigation: Ask the agent to include source links, collection dates, and source priority for each material claim.

Risk: Business, legal, financial, or reputational conclusions may be incomplete or outdated.

Mitigation: Verify important claims against official registries, regulator sites, court records, and other authoritative sources before making decisions.

Risk: Searched company names and business-intelligence intent may be sent to a local Baidu search helper.

Mitigation: Review the local search helper and avoid submitting sensitive, confidential, or personal information through the skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/tiandaox/skills/tianji-business-search)
- [Search tips](references/search-tips.md)
- [Business information sources](references/sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with search guidance and source-review notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include company names, query intent, public-source summaries, collection time, risk notes, and recommended verification steps.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
