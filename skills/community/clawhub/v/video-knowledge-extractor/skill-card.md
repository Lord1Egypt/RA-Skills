## Description: <br>
从视频、音频、播放列表或本地文件中抽取知识，生成摘要、要点、章节和适合知识库沉淀的 Markdown/JSON。适用于链接、文件路径和文件夹输入。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[louisshao464](https://clawhub.ai/user/louisshao464) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and knowledge workers use this skill to turn video, audio, playlists, local files, or folders into reusable knowledge-base notes, summaries, chapters, action items, and structured JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Folder inputs may recursively process more local media files than intended. <br>
Mitigation: Use narrow, intentional file and folder inputs and review the batch report after processing. <br>
Risk: When LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL are configured, transcripts, source paths or URLs, and related metadata may be sent to the configured LLM provider. <br>
Mitigation: Leave LLM_* environment variables unset for local-only processing, or use only a trusted LLM provider approved for the media content. <br>
Risk: The workflow depends on external tools for media download and transcription. <br>
Mitigation: Install yt-dlp and Whisper only from trusted sources and keep those tools updated. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/louisshao464/video-knowledge-extractor) <br>
- [README.md](README.md) <br>
- [examples.md](examples.md) <br>
- [output_templates/](output_templates/) <br>
- [scripts/process_media.py](scripts/process_media.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown and JSON files, including summary.md, notes.md, chapters.md, knowledge.json, manifest.json, and batch reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run with local fallback summaries when LLM settings are absent or post-processing fails; long transcripts may be truncated or chunked for LLM processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
