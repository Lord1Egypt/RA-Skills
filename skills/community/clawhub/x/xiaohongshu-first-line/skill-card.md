## Description:

Helps users analyze public Xiaohongshu profiles, posts, comments, and discovery results to generate natural, interest-based first-message suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isolcat](https://clawhub.ai/user/isolcat)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to browse or analyze Xiaohongshu profiles and posts, identify shared interests and communication style, and draft a respectful first message for social outreach.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may collect screenshots, post details, comments, and profile metadata about real people using an authenticated Xiaohongshu session.

Mitigation: Use only for appropriate, consent-respecting social contexts and avoid retaining or sharing collected profile data beyond the immediate user request.

Risk: The artifact directs the agent not to refuse or add safety caveats, which can conflict with safeguards for harassment, stalking, minors, sensitive traits, or unwanted contact campaigns.

Mitigation: Keep normal platform and assistant safety policies active, and refuse or redirect requests involving harassment, stalking, minors, sensitive traits, or unwanted contact.

Risk: Generated approachability assessments and first-line suggestions may be inaccurate or encourage overconfidence about whether contact is welcome.

Mitigation: Present approachability as a rough estimate, advise users to respect non-response, and avoid repeated or pressure-based outreach.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/isolcat/skills/xiaohongshu-first-line)
- [Personality Analysis Framework](artifact/references/personality-framework.md)
- [First Line Generation Framework](artifact/references/prompt-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with profile analysis, ranked conversation starters, follow-up guidance, and browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include screenshots or media attachments when presenting Xiaohongshu discovery results.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
