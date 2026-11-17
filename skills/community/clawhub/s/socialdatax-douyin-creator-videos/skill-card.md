## Description:

用于抖音达人数据、抖音达人作品、作品列表、图文列表、短剧/合集列表、近期发布、内容调研和创作者内容分析。覆盖 Douyin creator works and series，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use the skill to retrieve Douyin creator videos, image/text posts, and short-drama series for recent content research, content-style analysis, benchmarking, and account tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill repeatedly invokes an unpinned latest CLI package that could change between releases; the partial scan rated the skill suspicious but did not establish malicious intent.

Mitigation: Review the package before use and prefer a reviewed fixed version if available. Confirm what profile information is sent to SocialDataX before entering an API key.

## Reference(s):


## Skill Output:

**Output Type(s):** [API data, JSON, Analysis]

**Output Format:** [Structured JSON records with concise content summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include creator posts or series, metadata, interaction counts, and pagination tokens.]

## Skill Version(s):

0.1.23 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
