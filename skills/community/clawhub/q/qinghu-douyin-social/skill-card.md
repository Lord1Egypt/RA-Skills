## Description:

Helps agents perform Douyin social media operations with Qinghu data APIs, covering trend discovery, topic and video analysis, creator audience portraits, audience-fit checks, and executable content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, and agents use this skill to research Douyin trends, compare creator audiences with target customers, extract content angles from videos and comments, and produce actionable content plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Douyin-related requests and the user's Qinghu API token to Qinghu services.

Mitigation: Use only with a Qinghu token the user has authorized for this purpose, and avoid providing unrelated sensitive data in requests.

Risk: Approved tool calls may consume Qinghu credits.

Mitigation: Obtain user consent before calling Qinghu tools and report consumption using the returned pointCost value when available.

Risk: Large result sets may be exported or cached in local files.

Mitigation: Share only intended export links or summaries and handle generated local files according to the workspace's data retention expectations.

Risk: Broad activation wording can trigger the skill for generic Douyin brainstorming that does not need external data.

Mitigation: Use the skill when data-backed Douyin analysis is needed; otherwise provide general planning guidance without Qinghu API calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-douyin-social)
- [AutoAGC publisher profile](https://clawhub.ai/user/autoagc)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples, shell/API call instructions, concise recommendations, and optional exported data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce spreadsheet exports or use cached local data files for larger returned datasets.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
