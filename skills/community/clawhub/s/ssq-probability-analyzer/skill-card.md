## Description:

Helps users explore China's Double Color Ball lottery through entertainment-only number picks, expert-view summaries, draw checks, and explanations of why historical patterns cannot predict wins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmily741963](https://clawhub.ai/user/hmily741963)

### License/Terms of Use:

MIT-0

## Use Case:

Lottery players and their assistants use this skill to review public draw information, generate entertainment-only picks, check tickets against results, and understand lottery odds and costs. It does not offer a winning strategy or a basis for financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background scheduling and system inspection can create persistent activity or run with elevated privileges.

Mitigation: Run manually under a limited user account first; enable scheduled tasks or watchdogs only after reviewing their privileges and behavior.

Risk: Web data fetching and desktop report writes may expose activity or create local files unexpectedly.

Mitigation: Review network sources and report destinations before running; use the offline option when web access is unwanted.

Risk: Lottery analysis and number picks can be mistaken for reliable predictions.

Mitigation: Present picks as entertainment only, confirm current draw results independently, and avoid treating any output as a financial return strategy.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/hmily741963/skills/ssq-probability-analyzer)
- [Methodology](references/methodology.md)
- [Responsible play](references/responsible_play_2026.md)
- [Operations](references/operations.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, HTML report]

**Output Format:** [Text responses and a self-contained HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save the report to the desktop; offline data can be stale. Picks are for entertainment, not prediction.]

## Skill Version(s):

2.1.53 (source: ClawHub release, skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
