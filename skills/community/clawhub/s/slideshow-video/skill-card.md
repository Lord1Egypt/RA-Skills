## Description:

Generates short-form slideshow guidance, reusable JSON project configuration, and commands for producing PNG slides, voice-synced assets, and MP4 exports from local images, remote images, image queries, or GPT Image 2 visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn structured project JSON, image sources, and narration plans into short-form slideshow assets and MP4 exports for TikTok, Reels, Shorts, and similar channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated videos may be steered toward the default Clawlite.ai call-to-action.

Mitigation: Remove or override the default CTA and verify that the final slide and final narration line match the intended campaign.

Risk: Project JSON can trigger network access, session-backed image generation, remote media downloads, and file writes.

Mitigation: Run only trusted project JSON, avoid sensitive prompts or private URLs, pin OPENCLAW_BASE_URL to a trusted local endpoint, and use a constrained output directory.

Risk: Query-based or third-party hosted images can introduce quality, licensing, or brand-safety issues.

Mitigation: Prefer local approved images and audio for production, review resolved images before publishing, and validate third-party media rights before commercial use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/x-rayluan/skills/slideshow-video)
- [Slideshow Workflow](artifact/references/workflow.md)
- [Pipeline Example JSON](artifact/references/pipeline.example.json)
- [Slides Config Example JSON](artifact/references/slides-config.example.json)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When the bundled scripts are run, they can produce PNG slides, MP4 videos, resolved project JSON, cached media files, summary JSON, and sync metadata.]

## Skill Version(s):

0.2.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
