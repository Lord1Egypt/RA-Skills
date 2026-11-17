## Description:

Helps Bilibili social-media operators use Qinghu data to identify topics, deconstruct long-form video scripts, assess comments and sentiment, and match high-affinity UP creators for seeding campaigns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, social-media operators, and agent users use this skill to plan Bilibili content and creator campaigns from Qinghu API data. It supports topic discovery, long-form video script analysis, comment sentiment review, UP creator matching, and concise campaign recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require a Qinghu API token for Bilibili data lookups.

Mitigation: Use a scoped token where possible and avoid sharing exported outputs that contain sensitive account or campaign information.

Risk: Qinghu API calls may incur point charges.

Mitigation: Confirm planned tool calls before execution and report observed Qinghu point consumption after paid calls.

Risk: Large result sets may be exported to local files.

Mitigation: Review exported files before sharing them and remove files that are no longer needed.

Risk: Campaign recommendations depend on the returned Bilibili sample and may be incomplete if comments or creator data are limited.

Mitigation: State the platform, period, and sample size with conclusions, and avoid overgeneralizing beyond the queried data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-bilibili-social)
- [Qinghu data API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu login](https://www.iqinghu.com/workbench/login?type=1&urlCode=1788417429126)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)
- [Qinghu workflow permission check](https://www.iqinghu.com/api/desktop/qh/workflow/page?pageNum=1&pageSize=5)

## Skill Output:

**Output Type(s):** [guidance, markdown, files]

**Output Format:** [Concise Markdown recommendations with optional exported table files for larger result sets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes metric context such as platform, period, and sample size; reports Qinghu point consumption when paid calls are made.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
