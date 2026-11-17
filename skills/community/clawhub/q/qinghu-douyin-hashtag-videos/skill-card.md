## Description:

按抖音话题 ID 获取话题下的视频列表，支持排序和游标翻页。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Users and analysts can retrieve Douyin hashtag videos to review popular posts, sort results, and page through a topic's videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading qhkit and Node tooling changes the local environment.

Mitigation: Review installation steps and prefer a controlled environment with preinstalled, pinned qhkit.

Risk: Persisting a Qinghu API token on the machine can expose account access.

Mitigation: Configure the token only with user consent and avoid persistent storage unless it meets the user's security expectations.

Risk: Video queries can incur variable credit charges, especially when retrieving many results.

Mitigation: Check the current estimate, disclose expected charges, and obtain consent before paid calls or further pagination.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-douyin-hashtag-videos)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise text or Markdown summary; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports sorted, cursor-paginated results and reports credits charged for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
