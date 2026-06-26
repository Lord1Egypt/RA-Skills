## Description: <br>
Creates dark motivational TikTok/Reels videos by generating a timed script, producing an ElevenLabs voiceover, fetching real cinematic clips from Pexels, adding animated text overlays, applying FFmpeg color grading, and exporting a 1080x1920 MP4. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thuongvh2-python](https://clawhub.ai/user/thuongvh2-python) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators, marketers, and automation developers use this skill to assemble short dark-motivation social videos from user-provided topics, provider API keys, and real stock footage. It is suited for producing ready-to-post vertical MP4s with voiceover, captions, text timing, and cinematic grading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provider API keys and usage may expose cost, quota, or account risk when running the pipeline. <br>
Mitigation: Keep API keys out of source control, use a dedicated project folder, and monitor Anthropic, ElevenLabs, and Pexels usage or billing. <br>
Risk: Generated scripts, topics, or voice content may include private plans, personal data, or unauthorized voice cloning. <br>
Mitigation: Avoid private business plans or personal data in prompts and use voice cloning only with explicit authorization. <br>
Risk: Downloaded stock footage and generated captions may need review before posting. <br>
Mitigation: Review the final MP4, captions, and Pexels attribution before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thuongvh2-python/tiktok-motivation-video) <br>
- [Pexels API](https://www.pexels.com/api/) <br>
- [Anthropic Messages API endpoint](https://api.anthropic.com/v1/messages) <br>
- [ElevenLabs text-to-speech endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id}) <br>
- [Voice catalog](elevenlabs_voices.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code, shell commands, environment variables, and generated MP4 video artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The workflow depends on Anthropic, ElevenLabs, Pexels, MoviePy, pydub, FFmpeg, and API keys supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
