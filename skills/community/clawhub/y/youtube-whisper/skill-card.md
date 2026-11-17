## Description:

YouTube影片一鍵轉文字！自動下載影片並用AI轉成中文/英文字幕，沒有字幕的影片也能用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[dolphins1123](https://clawhub.ai/user/dolphins1123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to download or inspect YouTube subtitles and produce transcript text with local Whisper when subtitles are unavailable. Agents may return the transcript directly, summarize it, or point users to the transcript file for longer output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script downloads YouTube audio and writes transcript files locally, so output paths and existing files can be affected.

Mitigation: Run it in a reviewed workspace, choose explicit output paths, and check for existing files before execution.

Risk: Documented media limits are not enforced, and untrusted or very long media can create resource or reliability issues.

Mitigation: Use reviewed media inputs, avoid very long videos unless necessary, and monitor runtime, storage, and memory use.

Risk: Local dependencies such as yt-dlp, ffmpeg, and openai-whisper can change behavior across versions.

Mitigation: Install reviewed or pinned dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dolphins1123/skills/youtube-whisper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown response with transcript text, processing summary, and a local transcript file path when output is long.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local yt-dlp, ffmpeg, and openai-whisper; long transcript output may be written to a text file.]

## Skill Version(s):

1.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
