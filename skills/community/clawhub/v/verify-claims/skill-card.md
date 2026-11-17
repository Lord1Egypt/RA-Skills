## Description:

Verify claims and information using professional fact-checking services.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asgraf](https://clawhub.ai/user/asgraf)

### License/Terms of Use:


## Use Case:

External users use this skill to verify factual claims in articles, videos, transcripts, news, social posts, and other shared content by comparing relevant professional fact-checking sources and presenting an objective synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send user-provided claim text to external search and fact-checking sites.

Mitigation: Use the skill only for claims the user is comfortable sharing externally, and redact sensitive details before searching when possible.

Risk: For very recent claims, the skill may schedule follow-up checks and retain the original query, claims, and context.

Mitigation: Ask for explicit user consent before scheduling follow-up checks or retaining claim text, especially for fresh or sensitive claims.

## Reference(s):

- [List of fact-checking websites](https://en.wikipedia.org/wiki/List_of_fact-checking_websites)
- [ClawHub skill page](https://clawhub.ai/asgraf/skills/verify-claims)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with citations and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verdict summaries, uncertainty notes, relevant fact-checking links, and follow-up reminder text when scheduling is available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
