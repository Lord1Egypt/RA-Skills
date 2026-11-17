## Description:

从视频、音频、播放列表或本地文件中抽取知识，生成摘要、要点、章节和适合知识库沉淀的 Markdown/JSON。

This skill is ready for commercial/non-commercial use.

## Publisher:

[louisshao464](https://clawhub.ai/user/louisshao464)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn video, audio, playlists, local files, or folders into reusable knowledge-base notes with summaries, key points, chapters, action items, and structured JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured remote LLM endpoints may receive transcript content and local path metadata.

Mitigation: Use a dedicated input folder, avoid sensitive recordings unless remote LLM variables are unset or controlled, and use trusted HTTPS endpoints with narrowly scoped API keys.

Risk: Recursive folder processing can read every supported media file under a provided directory.

Mitigation: Point the skill at narrowly scoped folders and review generated transcript and knowledge files before sharing them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/louisshao464/skills/video-knowledge-extractor)
- [README.md](README.md)
- [examples.md](examples.md)
- [Output templates](output_templates/)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, configuration, guidance]

**Output Format:** [Markdown files, JSON files, transcript text, and processing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include summary.md, notes.md, chapters.md, knowledge.json, manifest.json, and transcript artifacts under the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
