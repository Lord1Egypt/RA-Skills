## Description: <br>
Real-time news intelligence from theshort.ai for searching topic- and tag-scoped feeds, fetching article details with summaries, and listing available topics and tags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sssemil](https://clawhub.ai/user/sssemil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to ground responses in recent curated news, search by topic or tag, retrieve article summaries, and cite source links for verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a scoped theshort.ai API key and can consume paid credits when news lookups are made. <br>
Mitigation: Use a limited, revocable key, monitor credit usage, and confirm the user is comfortable with billable calls before using credit-consuming endpoints. <br>
Risk: The billing-balance instruction is under-documented in the security evidence. <br>
Mitigation: Do not call the billing endpoint unless the provider documents its authorization model and returned data. <br>


## Reference(s): <br>
- [The Short News on ClawHub](https://clawhub.ai/sssemil/theshort-news) <br>
- [sssemil publisher profile](https://clawhub.ai/user/sssemil) <br>
- [theshort.ai external API](https://theshort.ai/api/external) <br>
- [OpenClaw dashboard](https://openclaw.theshort.ai) <br>
- [API key dashboard](https://openclaw.theshort.ai/dashboard/keys) <br>
- [Credits dashboard](https://openclaw.theshort.ai/dashboard/credits) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with API examples, JSON response shapes, and citation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include sourceName and canonicalUrl when summarizing news.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
