## Description:

Used to generate post-match reviews of World Cup football matches, and supports standardized scene input, post-match information retrieval and fan group notification extraction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vivalavida-say-hi](https://clawhub.ai/user/vivalavida-say-hi)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to generate concise World Cup football match reviews, including one-sentence summaries, match flow analysis, best-performer notes, and post-match talking points. When requested, it can incorporate relevant fan-group notification signals while avoiding unsupported or fabricated claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local notifications when fan-group discussion is relevant to the requested post-match review.

Mitigation: Specify the match, time range, groups or apps, and preferred language so notification retrieval is scoped to the intended context.

Risk: Post-match reviews can become misleading if live, unfinished, or weakly verified match information is treated as final.

Mitigation: Confirm match status first and use current-score or pre-game wording until a final score is verified.

Risk: Fan comments, notification snippets, or tactical interpretations could be mistaken for facts.

Mitigation: Separate facts, public opinion, and inference, and omit unsupported rumors or fabricated quotes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vivalavida-say-hi/skills/yoooclaw-world-cup-post-match-review-scene-en)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs only the requested review content and may vary structure by match status and requested review type.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
