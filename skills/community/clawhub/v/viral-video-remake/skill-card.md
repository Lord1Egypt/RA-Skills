## Description:

Analyzes a video link and its transcript and visual structure, then drafts an original video brief that borrows pacing without reusing the source content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackchew7143](https://clawhub.ai/user/jackchew7143)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and video teams use this skill to analyze the hook, pacing, and structure of a public video, then prepare an original script brief for their own topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review notes a mismatch between advertised and implemented features, so some links or breakdown details may not be available as described.

Mitigation: Check that the specific link is readable and review the returned analysis before using it to plan a video.

Risk: The security review advises considering retrieval features, environment data used in network requests, and undeclared tool scope.

Mitigation: Review the skill's access and network behavior before installation, and keep the LinkDigest API key in protected environment configuration.

## Reference(s):

- [LinkDigest documentation](https://linkdigest.dev/zh/docs?ref=skill-viral-video-remake)
- [ClawHub release page](https://clawhub.ai/jackchew7143/skills/viral-video-remake)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Markdown or JSON analysis, followed by a Markdown video brief]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a LinkDigest API key; video breakdown adds one credit.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
