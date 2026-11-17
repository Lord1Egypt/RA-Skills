## Description:

从小红书、马蜂窝、携程和微信公众号等多平台抓取评分最高的旅游攻略，按平台优先级、发布时间和季节权重整合为综合旅行攻略文档。

This skill is ready for commercial/non-commercial use.

## Publisher:

[whhh1994](https://clawhub.ai/user/whhh1994)

### License/Terms of Use:

MIT-0

## Use Case:

Travel planners and content operators use this skill to collect recent, high-signal travel guides from specified Chinese travel and social platforms, preserve source-specific metrics, and produce a consolidated Markdown itinerary or destination guide. It is intended for agent workflows that can coordinate subagents, browser access, local task files, and user review when anti-automation checks appear.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The launcher and browser workflow create review-worthy local execution and authenticated-browser risks.

Mitigation: Review the skill before installation, run it with a low-privilege browser profile or account, and close unrelated authenticated tabs before connecting CDP.

Risk: Destination inputs and harvested page text may be untrusted.

Mitigation: Use trusted destination inputs, keep the skill's source-platform constraints intact, and review generated travel guidance and source links before publishing or acting on them.

Risk: The workflow can evaluate an external xiaohongshu-crawler extraction script in the browser.

Mitigation: Verify the extraction script before allowing browser eval and avoid running the launcher on untrusted text.

Risk: Anti-automation checks, redirects, or platform blocks can interrupt collection or produce incomplete data.

Mitigation: Pause on CAPTCHA or redirect events, request user confirmation or specific article URLs, and mark partial platform results clearly in the final guide.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/whhh1994/skills/tourism-guide-harvester)
- [ClawHub publisher profile](https://clawhub.ai/user/whhh1994)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown travel-guide reports with source links, local task/status/data file templates, and inline shell or browser-command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Coordinates multi-platform collection, source weighting, mention counts, seasonal recency weighting, and final guide generation under user review.]

## Skill Version(s):

1.5.0 (source: release evidence and artifact/SKILL.md version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
