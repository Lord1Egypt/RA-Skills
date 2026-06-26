## Description: <br>
Extract sentiment patterns, repeated pain points, and feature requests from customer reviews to prioritize product fixes and copy improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leooooooow](https://clawhub.ai/user/leooooooow) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, product teams, and ecommerce operators use this skill to turn customer review corpora into aspect sentiment, ranked pain points, feature requests, and prioritized product or listing-copy actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer reviews may contain names, order details, or other personal information. <br>
Mitigation: Use the skill's de-identification guidance before sharing quotes externally and keep review IDs traceable without exposing personal data. <br>
Risk: Analysis may overstate patterns when the corpus is small, biased, duplicated, incentivized, or poorly segmented. <br>
Mitigation: Apply the quality checklist: record pulled and analyzed counts, remove duplicates, flag fake or incentivized reviews, segment by variant and time, and report confidence and coverage gaps. <br>
Risk: Automated sentiment coding can mishandle sarcasm, negation, star-text mismatches, or multi-aspect reviews. <br>
Mitigation: Code from review text, use the sentiment guide, log star-vs-text mismatches, and hand-verify a random sample before treating findings as decision-ready. <br>


## Reference(s): <br>
- [Review Analyzer on ClawHub](https://clawhub.ai/leooooooow/review-analyzer) <br>
- [Review Analysis Report Template](references/output-template.md) <br>
- [Sentiment Coding Guide](references/sentiment-coding-guide.md) <br>
- [Pain-Point Taxonomy](references/pain-point-taxonomy.md) <br>
- [Review Analysis Quality Checklist](assets/quality-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown report with tables, ranked findings, feature requests, and prioritized action lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a review corpus; supports de-identified quotes, review IDs, denominators, and baseline tracking.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
