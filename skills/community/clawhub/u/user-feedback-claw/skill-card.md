## Description: <br>
用户反馈虾 helps an agent analyze user reviews, complaints, support tickets, and survey feedback to extract sentiment, themes, priorities, and product improvement recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product, operations, and support teams use this skill to turn multi-channel feedback into a structured report of top issues, representative comments, trends, and recommended actions. It is most useful for Chinese-language ecommerce, customer service, NPS, and open-ended survey feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer reviews, support tickets, and survey responses may include personal data or sensitive business information. <br>
Mitigation: Redact names, account identifiers, contact details, and confidential business context before analysis. <br>
Risk: Small datasets, dialect-heavy text, slang, or noisy comments can reduce sentiment and theme accuracy. <br>
Mitigation: Label low-sample analyses as directional, review representative examples manually, and validate the highest-priority findings before acting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tujinsama/user-feedback-claw) <br>
- [Improvement templates](references/improvement-templates.md) <br>
- [Issue taxonomy](references/issue-taxonomy.md) <br>
- [Sentiment lexicon](references/sentiment-lexicon.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with prioritized issue lists, representative feedback excerpts, trends, and action recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Works from pasted text, CSV/Excel-style tabular feedback, or mixed feedback summaries; no code execution is required by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
