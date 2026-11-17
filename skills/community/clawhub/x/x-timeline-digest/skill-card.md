## Description:

Build a deduplicated digest from X (Twitter) For You and Following timelines using bird. Outputs a payload for upstream delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seandong](https://clawhub.ai/user/seandong)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to collect authenticated X/Twitter timeline items, remove duplicates and low-value posts, and produce a digest payload for review or downstream summarization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads authenticated X/Twitter For You and Following timelines and stores tweet IDs locally for deduplication.

Mitigation: Install only when this access is acceptable, keep the local state file protected, and review retention expectations before deployment.

Risk: Timeline content and generated digest text may be untrusted when passed into an LLM or downstream workflow.

Mitigation: Treat tweet text and links as untrusted input, review summaries before use, and avoid automatic posting or actions based on the output.

Risk: Bundled sample digest files may contain stale or user-specific timeline content.

Mitigation: Remove or replace sample digest outputs before publication or deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seandong/skills/x-timeline-digest)
- [Publisher profile](https://clawhub.ai/user/seandong)
- [Skill homepage](https://github.com/seandong)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [JSON payload with digestText, counts, window metadata, and tweet items; optional Simplified Chinese Markdown brief via the prompt template.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the bird CLI with an authenticated X/Twitter session and stores local tweet IDs for deduplication.]

## Skill Version(s):

1.0.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
