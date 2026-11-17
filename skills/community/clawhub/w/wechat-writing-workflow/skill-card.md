## Description:

Standardized WeChat official account writing workflow integrating wechat-publisher, wechat-toolkit, wechat-mp-writer-skill and other skills. Provides complete workflow from material search to publishing with 5 stages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[earthwalking](https://clawhub.ai/user/earthwalking)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and operators use this skill to plan and run a WeChat official account publishing workflow from material search through drafting, formatting, publishing, and post-publication analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can guide live posting, scheduled publishing, or mass sending to a WeChat official account.

Mitigation: Require human review and approval of every draft, preview, schedule, publish, or mass-send action before using connected publishing tools.

Risk: The workflow includes similarity-obscuring rewrite guidance that could be used to evade originality or attribution expectations.

Mitigation: Avoid washing or similarity-evasion steps; require original writing, accurate attribution, and editorial review before publication.

Risk: Publishing workflows may involve WeChat AppID and AppSecret credentials.

Mitigation: Store WeChat secrets outside drafts and shared files, restrict access to credentialed environments, and rotate secrets if exposure is suspected.

Risk: The workflow references external dependency installs for related tooling.

Mitigation: Use pinned versions or isolated environments when installing supporting tools such as npm packages.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/earthwalking/skills/wechat-writing-workflow)
- [WeChat Official Account documentation](https://developers.weixin.qq.com/)
- [wenyan-cli](https://github.com/wenyan-md/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown workflow guidance with command examples and configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces article drafts, title suggestions, summaries, cover-image recommendations, publishing status guidance, and data-analysis report guidance.]

## Skill Version(s):

1.0.1 (source: server release evidence and openclaw.skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
