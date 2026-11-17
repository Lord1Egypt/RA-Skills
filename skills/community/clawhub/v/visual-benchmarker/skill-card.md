## Description:

Visual Benchmarker is a meta-skill that guides an agent to find Douyin benchmark videos and analyze visual style for a project.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahsbnb](https://clawhub.ai/user/ahsbnb)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, creative, and content teams use this skill to turn project or product materials into Douyin search keywords, retrieve candidate videos through a separate search skill, and compile visual-style benchmark cases for planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords can expose confidential client, product, personal, or unreleased strategy details to the external search integration.

Mitigation: Redact sensitive information before extracting keywords or running Douyin searches; confirm keywords with the user when needed.

Risk: Benchmark quality depends on keyword quality and the separate douyin-video-search integration.

Mitigation: Review and adjust keyword sets before relying on selected videos for visual direction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahsbnb/skills/visual-benchmarker)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Markdown]

**Output Format:** [Markdown report with benchmark video links and concise visual analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes at least 3 recommended videos with links, highlights, and reusable visual elements.]

## Skill Version(s):

1.0.0 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
