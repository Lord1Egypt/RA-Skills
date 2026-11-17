## Description:

Provides summaries of public WeChat Channels video, topic, account, and leaderboard pages for lightweight engagement analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawkk](https://clawhub.ai/user/clawkk)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and operators use this skill to summarize public WeChat Channels pages, compare recent video engagement, and produce lightweight topic or leaderboard statistics. It is scoped to public content and excludes login automation, private data access, interface reverse engineering, and bypassing platform controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misused to process private account data or automate authenticated WeChat activity.

Mitigation: Use it only for public WeChat Channels pages and avoid login automation, private data collection, reverse engineering, or bypassing platform controls.

Risk: Repeated collection from dynamic pages can create platform compliance or rate-limit concerns.

Mitigation: Keep requests rate-limited, wait for rendered public content before summarizing, and follow applicable platform and information security rules.

## Reference(s):

- [WeChat Channels](https://channels.weixin.qq.com/)
- [ClawHub skill page](https://clawhub.ai/clawkk/skills/wechat-video)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise structured text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should stay limited to public page information and include source links or collection times when available.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
