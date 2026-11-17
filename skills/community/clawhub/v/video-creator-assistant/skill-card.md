## Description:

Video Creator Assistant helps agents plan video topics, draft scripts, design storyboards, polish copy, prepare subtitles and voiceover notes, adapt content for major Chinese social platforms, and analyze engagement opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and publishing teams use this skill to turn a topic, niche, or brief into platform-adapted video scripts, storyboards, titles, cover-copy suggestions, subtitles, and publishing guidance for short- and mid-form video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes an automatic learning system that can persist user preferences, notes, and usage metadata in learned_patterns.json.

Mitigation: Install only when local persistence is acceptable; require explicit approval before recording preferences or notes and review stored data regularly.

Risk: The artifact describes changing SKILL.md after repeated errors or usage thresholds, which can alter skill behavior over time.

Mitigation: Gate any skill-instruction changes behind human review, version control, and security scanning before deployment.

Risk: Trend analysis and platform recommendations may rely on time-sensitive WebSearch or WebFetch results.

Mitigation: Require source links and freshness dates for trend-based recommendations, and verify platform policy claims before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/video-creator-assistant)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured tables and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific guidance, freshness notes for referenced trends, and local learning records when the learning workflow is invoked.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
