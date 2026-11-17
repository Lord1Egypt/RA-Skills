## Description:

Chinese podcast analytics toolkit for discovering trending and rising podcasts or episodes, analyzing category competition, tracking subscription trends, and generating creator opportunity reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mteng27](https://clawhub.ai/user/mteng27)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, analysts, and developers use this skill to find Chinese podcast opportunities, compare shows or categories, monitor subscription and topic trends, and prepare concise reports grounded in public podcast ranking data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Xiaoyuzhou enrichment workflow may fetch arbitrary URLs when given untrusted input.

Mitigation: Use only canonical Xiaoyuzhou episode and podcast URLs, review URLs before enrichment, and add allow-list validation before enabling unattended use.

Risk: A tracking workflow may store invented subscriber history as if it were observed data.

Mitigation: Label generated history clearly, prefer observed API or page-derived measurements for reports, and review growth claims before sharing them.

Risk: The skill writes local JSON tracking files that may contain analysis state and public podcast metrics.

Mitigation: Run it in a workspace where local tracking files are expected, and review generated JSON files before publishing or sharing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mteng27/skills/xyz-podcast-radar-cn)
- [API Notes](references/api.md)
- [Output Modes](references/output-modes.md)
- [Title Signals](references/title-signals.md)
- [xyzrank ranking API](https://xyzrank.com/api/episodes)
- [xyzrank trend API](https://api.xyzrank.top/v1/stats)
- [Xiaoyuzhou](https://www.xiaoyuzhoufm.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries, JSON data, and shell commands for running bundled Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON tracking files for subscription, episode, and topic history.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
