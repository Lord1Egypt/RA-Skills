## Description:

Use RunningHub official standard-model APIs for image-to-video generation, including local media upload, task polling, and completed video download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[darker314159](https://clawhub.ai/user/darker314159)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to submit RunningHub image-to-video jobs from public image URLs or local image files, monitor completion, and retrieve generated videos. It is suited for workflows that need Wan 2.2, Kling v3.0 std, or Seedance 2.0 RunningHub endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local images and prompts are sent to RunningHub for processing.

Mitigation: Confirm every local file upload with the user and avoid submitting sensitive or confidential media.

Risk: The helper requires a RunningHub API key.

Mitigation: Use the RUNNINGHUB_API_KEY environment variable or a scoped key, and avoid exposing credentials in shared command history or logs.

Risk: The security scan reports unsafe handling of remote response values during output download.

Mitigation: Review downloads before installation and prefer a patched version that sanitizes downloaded filenames and blocks credential-bearing redirects.

Risk: RunningHub-hosted uploaded media and outputs may expire.

Mitigation: Download completed videos promptly and keep outputs in an explicit local directory.

## Reference(s):

- [RunningHub Video API Reference](references/api_reference.md)
- [RunningHub media upload endpoint](https://www.runninghub.cn/openapi/v2/media/upload/binary)
- [RunningHub task query endpoint](https://www.runninghub.cn/openapi/v2/query)
- [RunningHub publisher profile](https://clawhub.ai/user/darker314159)
- [ClawHub skill page](https://clawhub.ai/darker314159/skills/runninghub-video)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance, command examples, JSON status output, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RunningHub API key and may create local output files in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
