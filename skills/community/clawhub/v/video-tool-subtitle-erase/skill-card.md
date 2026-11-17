## Description:

Remove burnt-in subtitles or on-screen text from an HTTPS video via WeryAI (video-subtitle-erase). Use when the user wants subtitle or text removal, not translation or text-to-video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to remove burnt-in subtitles or on-screen text from an existing public HTTPS video with WeryAI. It supports optional normalized regions for targeted removal and is not for translation, watermark-only cleanup, or text-to-video generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid WeryAI runs can consume credits and send the public video URL plus request settings to WeryAI.

Mitigation: Use dry-run first, confirm the video URL and any custom regions with the user, and run submit or wait only after explicit approval.

Risk: The WERYAI_API_KEY could be exposed if stored in files or logs.

Mitigation: Keep WERYAI_API_KEY only in the runtime environment and do not write it into skill files, prompts, command examples, or generated artifacts.

Risk: Private or internal-only media URLs may be shared with the external provider if submitted.

Mitigation: Submit only public HTTPS videos that the user intends to process with WeryAI; do not submit private or internal URLs without explicit consent.

Risk: Running out-of-scope scripts from a mixed or over-broad install could invoke workflows outside subtitle erasure.

Mitigation: Verify the package layout and run only artifact/scripts/video_subtitle_erase.js for this skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-subtitle-erase)
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON command output from the WeryAI wrapper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include task IDs, status records, error objects, and final video URLs returned by WeryAI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
