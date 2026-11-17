## Description:

Automatically collects recent public X posts from configured AI creators, filters and summarizes them into bilingual briefings, drafts an English post, and can publish the result to X.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kelcey2023](https://clawhub.ai/user/kelcey2023)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and analysts use this skill to monitor selected AI creator accounts on X, turn recent public posts into concise Chinese and English briefings, draft short update posts, and optionally schedule publishing and archiving.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated posts can be published to X automatically without a human review step.

Mitigation: Change the runner and scheduled jobs to draft-only, review the final post text manually, and confirm which authenticated posting account will publish.

Risk: Briefings are based on scraped public X content, so results may be incomplete or affected by access limits and page changes.

Mitigation: Use conservative schedules and check each generated briefing for omissions, stale links, and inaccurate summaries before publishing or reusing it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kelcey2023/skills/zeelin-x-creator-briefing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration]

**Output Format:** [Markdown briefing files, plain-text tweet drafts, JSON run metadata, and shell command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can auto-publish when publishing is enabled; generated outputs are date-stamped and intended for review before posting.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
