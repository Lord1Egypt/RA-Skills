## Description: <br>
Automate YouTube video editing workflow: Download -> Transcribe (Whisper) -> Analyze (GPT-4) -> High-Quality Thumbnail (Korean & Character Consistency). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeong-wooseok](https://clawhub.ai/user/jeong-wooseok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Content creators and video production agents use this skill to turn YouTube or local videos into transcripts, Korean SEO metadata, and thumbnail assets with OpenAI and local media tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video audio and transcript-derived text may be sent to OpenAI services during transcription and analysis. <br>
Mitigation: Use only appropriate source videos, review data-handling requirements before execution, and prefer limited or revocable API keys. <br>
Risk: The skill runs local media and browser tooling and can optionally call the nano-banana-pro skill for image generation. <br>
Mitigation: Install and run it only in trusted environments, ensure FFmpeg and optional dependencies are expected, and review nano-banana-pro separately before enabling thumbnail generation. <br>
Risk: User-provided avatar or font file paths are read during thumbnail generation. <br>
Mitigation: Use trusted local asset paths and avoid untrusted avatar inputs until the local HTML escaping concern noted in the security guidance is fixed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands; generated subtitles, transcripts, Korean metadata, and thumbnail image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENAI_API_KEY; optionally uses NANO_BANANA_KEY, FFmpeg, Playwright, rembg, and local input assets.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
