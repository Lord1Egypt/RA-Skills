## Description:

Rolling multi-sport digest skill that tracks current storylines, recent results, upcoming fixtures/events, injuries/availability, and standings across a chosen sports portfolio while keeping a compact context file current.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ds215](https://clawhub.ai/user/ds215)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to produce recurring, concise sports digests for selected teams, leagues, tours, or competitions while maintaining a compact rolling context file for continuity across runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sports results, standings, injuries, and schedules can change quickly or conflict across sources.

Mitigation: Use current-session sources for every reported fact, prefer direct and current reports when sources conflict, and state uncertainty instead of inferring outcomes.

Risk: A rolling context file can become stale, misleading, or too large if old fixtures and storylines are appended indefinitely.

Mitigation: Replace outdated information, remove obsolete injuries and narratives, keep only context useful for the next digest, and update the last-updated date after meaningful changes.

Risk: A poorly configured sports scope, cadence, or delivery channel can produce irrelevant or misdirected digests.

Mitigation: Configure the sports scope, schedule, recipient, and delivery channel deliberately before use.

## Reference(s):

- [Sports Digest ClawHub Skill Page](https://clawhub.ai/ds215/skills/sports-digest)
- [SPORTS_CONTEXT.md Template](artifact/SPORTS_CONTEXT_template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown digest text and rolling context-file update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require current sports web research and deliberate configuration of scope, schedule, and delivery channel.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
