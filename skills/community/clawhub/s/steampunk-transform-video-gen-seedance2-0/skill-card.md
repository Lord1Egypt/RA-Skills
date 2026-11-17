## Description:

Rebuild any brief into Victorian-industrial steampunk: brass, wood, steam plumes, visible mechanisms--WeryAI Seedance 2.0 only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and developers use this skill to transform text briefs or a single image into short Victorian-industrial steampunk videos through WeryAI Seedance 2.0. It expands prompts, confirms generation settings, runs the bundled Node.js CLI, and returns playable video links or actionable failure details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WeryAI API key and sends prompts, image URLs, and chosen attachment files to WeryAI.

Mitigation: Use a scoped key where possible, keep the key out of committed files, and run the skill only when third-party video generation is acceptable.

Risk: A local image path may be read and uploaded to WeryAI as a public URL.

Mitigation: Prefer public HTTPS image URLs; use local paths only after verifying the exact file and obtaining explicit consent to upload it.

Risk: Video generation is a paid network operation that may consume credits on each run.

Mitigation: Show the full prompt and settings before submission, require confirmation, and avoid reruns unless the user approves the additional cost.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/steampunk-transform-video-gen-seedance2-0)
- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline links and JSON status or error details from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns playable video links when generation succeeds; may also provide task identifiers, status, or error codes from WeryAI.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
