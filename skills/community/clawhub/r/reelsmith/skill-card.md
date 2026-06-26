## Description: <br>
Reelsmith creates short-form vertical video packages, preview reels, narrated reels, and optional AI-video workflows from ideas, articles, updates, or source material. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[normandmickey](https://clawhub.ai/user/normandmickey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, social media operators, and developers use Reelsmith to turn topics into approval-ready Facebook Reels packages, rough vertical previews, narrated previews, or optional AI-generated video assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional helpers can create local media files and may overwrite selected output paths. <br>
Mitigation: Choose fresh output filenames and review paths before running preview, narration, muxing, or video-generation helpers. <br>
Risk: OpenAI TTS and LTX video helpers may send text or prompts to external AI services. <br>
Mitigation: Use non-sensitive text and prompts, and keep OPENAI_API_KEY and LTX_API_KEY scoped to the intended use. <br>
Risk: The skill relies on local ffmpeg and Python media helpers for preview and muxing workflows. <br>
Mitigation: Run the helpers only in a trusted local environment after reviewing the commands and installed dependencies. <br>


## Reference(s): <br>
- [Reelsmith on ClawHub](https://clawhub.ai/normandmickey/reelsmith) <br>
- [LTX text-to-video API endpoint](https://api.ltx.video/v1/text-to-video) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with optional bash commands and JSON scene specifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local MP4 or MP3 media files when helper scripts are run.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
