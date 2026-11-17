## Description:

Generate a 30-second cinematic ad video with consistent character, AI narration, brand overlays, and ambient music.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jytech2023](https://clawhub.ai/user/jytech2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to generate a short branded ad video from a storyboard, with AI-generated visuals, narration, captions, background music, and Cloudflare R2-hosted outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires Vidu, Wavespeed, Replicate, and Cloudflare R2 credentials.

Mitigation: Use least-privilege accounts, keep credentials out of prompts and logs, and rotate keys after testing or sharing the environment.

Risk: Generated and intermediate media assets are uploaded to an R2 public URL.

Mitigation: Use a dedicated bucket or prefix, avoid sensitive source material, and confirm that public sharing is intended before running the workflow.

Risk: Remote media downloads and provider polling are weakly constrained.

Mitigation: Validate polling hosts before sending provider tokens, add download size limits, and validate media files before ffmpeg processing.

Risk: Dependencies are declared without a lockfile in the artifact evidence.

Mitigation: Pin dependencies with a lockfile and review package updates before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jytech2023/skills/xpilot-ad-maker)
- [OpenClaw homepage](https://github.com/dotku/x-post-scheduler/tree/main/skills/xpilot-ad-maker)
- [Vidu Platform](https://platform.vidu.com)
- [Example final ad](https://pub-22e3d3e3f43e400493bbd71306cae6bb.r2.dev/demo/medical-tourism-ad/v2/medtravel-final.mp4)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell commands and generated MP4 asset URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow uploads the final ad and intermediate media assets to the configured Cloudflare R2 public URL.]

## Skill Version(s):

0.1.0 (source: release metadata, OpenClaw metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
