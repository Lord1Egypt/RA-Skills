## Description:

Grades the ripeness of crop fruits from images or videos using visible color, size, and gloss features.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

Growers and agricultural teams use this skill to assess fruit ripeness and inform harvest timing from images or short videos. It can also retrieve account-linked historical analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fruit images or videos are sent to a configured cloud analysis service.

Mitigation: Use only media approved for cloud processing and review the service's data-handling terms before uploading.

Risk: The skill creates or reuses local identity state, may persist service tokens, and queries account-linked report history in the cloud.

Mitigation: Protect and periodically review the workspace data directory; clear the generated database when retained identity or report history is unwanted.

Risk: The package includes generic or pet-analysis code that does not match the fruit-grading description.

Mitigation: Review bundled code and its actual behavior before installing or executing it.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/smyx-sunjinhui/skills/smyx-crop-fruit-ripeness-grading-analysis)
- [Fruit ripeness analysis API documentation](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Structured ripeness report or Markdown table of historical reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ripeness grades, harvest guidance, and report links; results should be checked against local grading standards.]

## Skill Version(s):

1.0.14 (source: ClawHub release; bundled skill frontmatter states 1.0.16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
