## Description: <br>
Segments a long-form video and matching SRT into 3-6 stand-alone topical short clips, producing raw clips and per-clip SRT files for downstream post-production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jianshuo](https://clawhub.ai/user/jianshuo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video producers use this skill to choose semantic topic boundaries from an SRT, cut source footage with ffmpeg, slice per-clip subtitles, and prepare raw clips for a separate overlay or post-production workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes helper scripts beyond the core video-cutting workflow, including post-production helpers that are not required for the declared segmentation handoff. <br>
Mitigation: Use the core segment.py workflow and burn_subs.py with --no-burn for SRT slicing; review helper scripts before running make_cover.py, prepend_intro.py, or other post-production helpers. <br>
Risk: The security scan notes an unsafe local ffmpeg lookup path that could run an unexpected binary. <br>
Mitigation: Set FFMPEG to a trusted binary or ensure PATH resolves to trusted ffmpeg and ffprobe executables before running the scripts. <br>
Risk: Cover-generation helpers may share frames or prompts with external image-generation tooling if run. <br>
Mitigation: Do not run make_cover.py unless external frame sharing and AI cover generation are approved for the source material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jianshuo/wjs-segmenting-video) <br>
- [Segments JSON schema](references/segments_schema.json) <br>
- [Example segments JSON](references/example_segments.json) <br>
- [Platform cover dimensions](references/platform_sizes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown guidance with JSON configuration and bash commands; generated artifacts are MP4 clips, SRT files, extracted frames, and segments.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a source video, matching SRT, ffmpeg/ffprobe, and user confirmation before orientation conversion.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
