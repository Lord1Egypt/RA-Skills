## Description:

Replace or move an element in an existing HTTPS video with WeryAI anime-style processing (video-anime-replace). Use when the user wants anime-style object replace or move on a video URL, not text-to-video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run WeryAI anime-style replace or move jobs on an existing public HTTPS video with a public HTTPS reference image. It is scoped to the video-anime-replace workflow and excludes text-to-video, image-to-video, local file upload, and other WeryAI video-tool endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends public video and image URLs to WeryAI and uses WERYAI_API_KEY for potentially paid jobs.

Mitigation: Use dry-run first, confirm the URLs and non-default options with the user, and keep WERYAI_API_KEY only in the runtime environment.

Risk: Running out-of-scope scripts or passing local file paths could expand the data-sharing behavior beyond this skill's contract.

Mitigation: Run only scripts/video_anime_replace.js for this skill and use only public https:// video_url and image_url inputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-anime-replace)
- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return dry-run request previews, task IDs, status JSON, and Markdown video links after a completed WeryAI job.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
