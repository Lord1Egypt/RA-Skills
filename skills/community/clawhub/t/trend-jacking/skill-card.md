## Description:

Helps an agent evaluate a proposed social media trend for brand fit, safety, and timing, then produce an on-brand remix or refusal guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing and social media teams use this skill to decide whether a specific trend is worth joining and to shape a fast, brand-safe response. It supports trend vetting, refusal decisions, and handoff-ready content direction for short video, captions, carousels, and scheduling workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A trend response could be published publicly without the right human approval.

Mitigation: Define approval rules before connecting this skill to any posting or scheduling workflow, and require review for public content.

Risk: The skill could appear to identify current trends even though live trends change quickly.

Mitigation: Use current platform or social listening sources for discovery, then use this skill to vet and adapt the specific trend.

Risk: Joining tragedies, divisive moments, harmful origins, or sensitive cultural events can create ethical and reputational harm.

Mitigation: Apply the safety gate first, refuse opportunistic trend-jacking in hard-no areas, and redirect to non-promotional help or safer on-brand options.

Risk: Brand accounts may misuse sounds, memes, likenesses, or formats without checking commercial rights or fit.

Mitigation: Verify rights and platform rules for commercial use, and route meme-format or IP/likeness questions to a specialized culture or legal review workflow.

## Reference(s):

- [The Three Gates](references/the-three-gates.md)
- [Trend Types & Finding Them](references/trend-types-and-finding.md)
- [The Remix](references/the-remix.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text recommendations, refusals, and content handoff guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May route execution to related content and scheduling skills; does not provide live trend discovery or analytics.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
