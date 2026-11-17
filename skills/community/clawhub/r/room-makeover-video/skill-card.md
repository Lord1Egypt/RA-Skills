## Description:

Generates vertical WeryAI home makeover shorts for room refresh reels, including rental cream aesthetics, balcony cafe corners, themed kids' rooms, and strong before/after reveals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agent operators use this skill to turn room makeover briefs into validated WeryAI text-to-video or image-to-video runs. It helps prepare prompts and parameters, invoke the bundled Node.js CLI, and return playable video URLs or clear failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeryAI API key and sends prompts or images to WeryAI.

Mitigation: Install only when the operator accepts WeryAI processing, keep the API key out of the package, and prefer short-lived or isolated runtime environments.

Risk: Local image inputs can cause readable files to be uploaded to WeryAI.

Mitigation: Prefer public HTTPS image URLs; use local paths only after reviewing the exact file and obtaining explicit consent.

Risk: Shell examples can be unsafe if user prompts are interpolated directly into command strings.

Mitigation: Invoke the CLI with structured process arguments or another non-shell mechanism when handling user-supplied prompts.

## Reference(s):

- [WeryAI Video API CLI Reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub Skill Page](https://clawhub.ai/zoucdr/skills/room-makeover-video)
- [Publisher Profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown confirmation tables, shell commands, and JSON-derived video URL summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WeryAI task JSON to report task IDs, video URLs, cover URLs, or error codes.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
