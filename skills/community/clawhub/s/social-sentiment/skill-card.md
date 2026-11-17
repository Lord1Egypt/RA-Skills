## Description:

Analyzes public social-media posts from Twitter, Reddit, and Instagram to monitor brand and product sentiment, reputation trends, complaints, praise, and crisis signals at scale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External users, marketers, analysts, and developers use this skill to query Xpoz social data, export posts, classify sentiment, identify themes, and prepare brand-monitoring reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends brand and search queries to Xpoz and stores exported social-media CSVs locally.

Mitigation: Use it only where Xpoz use and the OAuth setup flow are approved, and treat downloaded CSVs as sensitive business or compliance data.

Risk: The skill depends on the mcporter npm package and the xpoz-setup authentication flow.

Mitigation: Review or pin mcporter in stricter environments and verify Xpoz access before running collection commands.

Risk: The example sentiment classifier is keyword-based and can misclassify nuanced, sarcastic, or context-dependent posts.

Mitigation: Review sample outputs, tune keywords for the brand and domain, and validate important conclusions before using them in reports.

## Reference(s):

- [Social Sentiment ClawHub Skill Page](https://clawhub.ai/atyachin/skills/social-sentiment)
- [Xpoz](https://xpoz.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, CSV handling steps, and report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include sentiment summaries, theme extraction guidance, viral-post review guidance, and local CSV export handling notes.]

## Skill Version(s):

1.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
