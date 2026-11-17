## Description:

Run RoughCut headlessly on macOS to generate Final Cut Pro (FCPXML) rough-cut timeline variants from a talking-head video - local-first, no media upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samergmtm22](https://clawhub.ai/user/samergmtm22)

### License/Terms of Use:


## Use Case:

External creators, editors, and agent operators use this skill to run a local macOS RoughCut workflow that turns talking-head videos into Final Cut Pro XML timeline variants. It supports local video files or direct HTTPS downloads and can optionally remove bad takes and off-topic content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local RoughCut repository script that may be unpinned or modified.

Mitigation: Install only from a trusted checkout, verify the repository origin and commit before execution, and avoid using an arbitrary configured repo_root.

Risk: Fluff removal may require a Gemini API key.

Mitigation: Provide GEMINI_API_KEY through a local environment variable only when fluff removal is explicitly enabled.

Risk: Direct download URLs and debug bundles may expose or derive from sensitive video content.

Mitigation: Treat direct video URLs and generated debug bundles as sensitive, limit sharing, and remove them when no longer needed.

## Reference(s):

- [ClawHub RoughCut skill page](https://clawhub.ai/samergmtm22/skills/roughcut-openclaw)
- [RoughCut local repository required by the skill](https://github.com/samerGMTM22/OpenClaw-RoughCut)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Markdown with inline bash code blocks and returned file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the generated RoughCut.xml_variants.zip path, the input video path, and optional download or debug bundle paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
