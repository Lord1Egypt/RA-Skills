## Description:

一个提供全面的跑步计算工具的MCP服务器，包括VDOT计算、训练配速、比赛时间预测、速度标记、心率区间和配速转换等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Runners, coaches, and agent users can use this skill to calculate VDOT, training paces, race-time predictions, velocity markers, heart-rate zones, and pace or speed conversions from supplied running data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends running and heart-rate inputs to a remote XiaoBenYang API.

Mitigation: Use it only when sharing those inputs with mcp.xiaobenyang.com is acceptable.

Risk: The API key is saved in a local .env file as plaintext.

Mitigation: Prefer secure secret storage where available and restrict access to the working directory.

Risk: Unrelated Gaokao and school-search remnants make the package identity and scope unclear.

Mitigation: Review or remove the unrelated remnants before relying on the skill in a trusted environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/running-formulas)
- [XiaoBenYang API key portal](https://xiaobenyang.com)
- [XiaoBenYang API endpoint](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, API Calls, guidance]

**Output Format:** [Markdown summaries of JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a XiaoBenYang API key and user-provided running or heart-rate inputs.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
