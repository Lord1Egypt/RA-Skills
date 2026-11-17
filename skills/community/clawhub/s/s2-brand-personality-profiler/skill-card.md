## Description:

S2 中国品牌个性量表演算模型。基于向忠宏 2010 年创立的“5维度-18层面-51人格”中国品牌个性量表，通过品牌搜索投影算法，为品牌进行精准的本土化人格定位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Brand strategists, marketers, and agents use this skill to analyze Chinese-market brand personality against the 5-18-51 model, estimate n-value deviations from industry averages, and produce positioning and audience-fit recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Numeric brand-personality scores may be based on web search results or simulated semantic estimates and can be mistaken for verified measurements.

Mitigation: Label estimates clearly, preserve sources for any search-derived counts, and have a human analyst review conclusions before using them for brand or marketing decisions.

Risk: The model is tailored to Chinese brand-personality constructs, which may limit its fit for brands or audiences outside that market context.

Mitigation: Use the output as Chinese-market positioning guidance and validate interpretations against local market research when applying it to other regions.

Risk: The skill may answer in Chinese by default, which can reduce reviewer understanding for non-Chinese-speaking teams.

Mitigation: Request the final report in the reviewer team's working language when needed and retain the original Chinese trait labels for traceability.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/spacesq/skills/s2-brand-personality-profiler)
- [ClawHub Publisher Profile](https://clawhub.ai/user/spacesq)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown analysis report with n-value findings, personality classification, and audience-fit recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use web search or simulated semantic estimates; numeric outputs should be treated as analytic approximations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
