## Description:

Analyzes Bilibili, Douyin, and Toutiao video links by downloading media, extracting frames, using a local minicpm-v model to describe frames, and producing an overall content summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murrayhoung](https://clawhub.ai/user/murrayhoung)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users can use this skill to process Chinese social-video URLs, extract representative frames, and summarize visible video content using a local vision model instead of a cloud API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can fetch broadly scoped URLs and overwrite user-writable files.

Mitigation: Restrict downloads to intended Bilibili, Douyin, and Toutiao domains, require confirmation before downloading media, stream with size limits, and write only inside a generated temporary directory with non-conflicting filenames.

Risk: The workflow downloads and processes third-party video content through browser automation and local files.

Mitigation: Use only video URLs the user is authorized to process, keep browser extraction scoped to the requested page, and clean up downloaded videos and extracted frames after analysis.

Risk: Extracted frames are sent to a local Ollama service for vision-model analysis.

Mitigation: Confirm the Ollama endpoint is local and trusted before use, and avoid processing sensitive videos unless local retention and access controls are acceptable.

## Reference(s):

- [Video download scripts](artifact/references/download.md)
- [ClawHub skill page](https://clawhub.ai/murrayhoung/skills/video-analyzer-cn)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands, Python snippets, and Chinese video-analysis summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single-stream workflow summary and frame-level descriptions; generated media files and extracted frames are local artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
