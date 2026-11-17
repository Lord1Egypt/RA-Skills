## Description:

用户反馈情感与痛点分析助手。批量分析用户评论、问卷开放题，做情感极性判断与痛点分类，输出设计评审洞察。

This skill is ready for commercial/non-commercial use.

## Publisher:

[20232931028](https://clawhub.ai/user/20232931028)

### License/Terms of Use:

MIT-0

## Use Case:

UX designers, researchers, and product teams use this skill to turn batches of app reviews, support tickets, and open-ended survey answers into sentiment labels, pain point categories, summary tables, and prioritized design recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User feedback may include sensitive personal data pasted into the active chat context.

Mitigation: Remove or anonymize personal data before analysis unless processing that data in the active chat context is acceptable.

Risk: Sentiment labels, pain point categories, and design recommendations are analytical inferences that may be misleading for small or biased samples.

Mitigation: Treat results as design-review input, preserve quoted user facts separately from inferences, and qualify conclusions when the sample is limited.

Risk: Feedback involving personal safety or regulated domains could require expert review beyond UX analysis.

Mitigation: Highlight safety-related feedback separately and avoid producing medical, financial, or other professional conclusions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown with per-feedback annotations, summary tables, ranked feedback lists, keyword counts, and concise recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language output by default; the final insight section is capped at 200 Chinese characters.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
