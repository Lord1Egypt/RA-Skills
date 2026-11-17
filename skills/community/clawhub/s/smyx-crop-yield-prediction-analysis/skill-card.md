## Description:

Predicts expected yield of economic crops such as tomato, corn and potato by combining growth stage, nutrition status, environmental data and historical yield references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze crop plant or field images and videos, estimate expected yield ranges and confidence, and retrieve prior crop-yield analysis reports for planning, supply-chain, market-matching, and agricultural insurance reference workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided crop images or videos, identity data, and report-history requests are sent to configured LifeEmergence/SMYX APIs.

Mitigation: Review configured endpoints before installation and only use the skill with media, identity linkage, and report data that are appropriate to send to those services.

Risk: The skill creates or reuses a local identity and stores access tokens in a workspace SQLite database.

Mitigation: Run it only in the intended workspace and avoid using it in shared workspaces that contain sensitive identity files unless that account linkage is intended.

Risk: Yield estimates may be incomplete or misleading when based on limited or low-quality crop images or videos.

Mitigation: Treat results as planning reference material and verify important yield, harvest, or insurance decisions with field measurements and applicable business rules.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-crop-yield-prediction-analysis)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [API 接口文档](references/api_doc.md)
- [API接口文档](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON text reports, with optional saved file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured yield estimates, confidence, influencing factors, report-history listings, and report links.]

## Skill Version(s):

1.0.8 (source: server release evidence; artifact frontmatter reports 1.0.9)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
