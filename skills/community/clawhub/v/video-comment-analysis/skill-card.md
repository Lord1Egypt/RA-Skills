## Description:

Analyzes short-video comment sections from a seller/operator perspective and produces business-focused findings, visible browsing notes, and polished HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mx9690](https://clawhub.ai/user/mx9690)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, sellers, and operators use this skill to review TikTok, Douyin, Instagram Reels, YouTube Shorts, or similar comment sections and identify demand, purchase intent, conversion blockers, selling drivers, and next-step optimizations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill defaults to Chinese-oriented seller/operator reports, which may not match every audience or market.

Mitigation: Ask the agent to use the desired report language, platform context, and market assumptions before analysis begins.

Risk: The workflow defaults to saving a report on the Desktop and opening it automatically.

Mitigation: Specify an alternate output path or request no auto-open behavior when local file placement or immediate browser opening is undesirable.

Risk: Business conclusions can be misleading if the visible comment sample is limited or replies are treated as main-comment statistics.

Mitigation: Review the report's sample boundaries, effective comment count, expanded reply-thread count, and methodology notes before acting on recommendations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mx9690/skills/video-comment-analysis)
- [Execution manual](artifact/references/execution-manual.md)
- [Visualization spec](artifact/references/visualization-spec.md)
- [Page skeleton](artifact/references/page-skeleton.md)
- [HTML report template](artifact/assets/html-report-template/index.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Files, Guidance]

**Output Format:** [Text or Markdown analysis with optional local HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should state sample boundaries, reply-thread usage, and which findings are counted metrics versus analyst judgment.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
