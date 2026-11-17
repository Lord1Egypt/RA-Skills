## Description:

A teaching/demo skill for news sentiment analysis that uses rule-based keyword scoring rather than a full NLP model and does not require a real-time news API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and agents use this skill to run a simple command-line news sentiment demo for stock codes, returning article counts and rule-based sentiment distribution for instructional or lightweight exploratory workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact Sina Finance using user-provided stock codes.

Mitigation: Run it only in environments where outbound access to that public site and disclosure of the queried stock codes are acceptable.

Risk: The sentiment output is simplified and can be misleading if treated as real market or NLP analysis.

Mitigation: Present results as illustrative teaching output and do not use them as investment advice or as a substitute for validated sentiment models.

Risk: Network failures or access limits can cause fallback behavior that does not reflect current news.

Mitigation: Check the reported processing mode and avoid relying on fallback/demo output for current-event decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yansheng-news-sentiment)
- [Sina Finance stock page template](https://finance.sina.com.cn/realstock/company/{code}/nc.shtml)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text report or JSON from a command-line Python script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sentiment scores are illustrative and based on simplified rules and keyword counts.]

## Skill Version(s):

1.0.5 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
