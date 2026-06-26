## Description: <br>
Ingest and summarize cross-platform videos into a local knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Exsusiai](https://clawhub.ai/user/Exsusiai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to turn YouTube, Bilibili, Xiaohongshu, and local media or subtitle files into transcripts, summaries, metadata, and local knowledge-base records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs, local media, transcripts, summaries, metadata, and downloaded artifacts can be retained in the local knowledge-base directory. <br>
Mitigation: Use --kb-root for project-specific storage, review retained files, and delete stored artifacts when retention is no longer acceptable. <br>
Risk: Private cookies or confidential media may be processed by the download, transcription, and summarization workflow. <br>
Mitigation: Avoid private cookies and confidential media unless the local retention and configured summarize/Codex processing model are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Exsusiai/video-knowledge-ingest) <br>
- [Toolchain Reference](references/toolchain.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON stdout plus local Markdown, text, and JSON files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes source metadata, transcript, summary, record, downloads, Whisper outputs, and an append-only index under the configured knowledge-base root.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
