## Description:

Generates concise Chinese-language FIFA World Cup football match reviews, including match-state handling, post-match summaries, tactical recap, standout-player discussion, and fan-message hot-topic synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to turn a World Cup football match, team, player, or post-match event into a shareable Chinese match review. It is also used to summarize relevant fan-group notifications when the user requests discussion trends or a full review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may query broad local notification and group-chat signals while preparing fan-discussion sections.

Mitigation: Specify exact apps, groups, and time ranges before running hot-topic or full-review requests.

Risk: Unrelated private or work notifications may be included if the scope is too broad.

Mitigation: Use the skill only where local notification access is acceptable, and avoid unrestricted searches on devices with sensitive unrelated notifications.

Risk: Live or not-yet-started matches can lead to premature post-match conclusions if match state is unclear.

Mitigation: The skill requires conservative match-state classification and uses live-status or pre-match formats until full-time status is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-world-cup-post-match-review-scene)
- [ClawHub publisher profile](https://clawhub.ai/user/vivalavida-say-hi)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-formatted Chinese match review text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill switches between post-match review, live-status update, and pre-match brief formats based on confirmed match state.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
