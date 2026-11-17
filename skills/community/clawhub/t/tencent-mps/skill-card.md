## Description:

Tencent MPS helps agents generate Tencent Cloud Media Processing Service commands for media processing, AI generation, content understanding, COS file operations, task queries, and usage reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-mpaas-skills](https://clawhub.ai/user/tencent-mpaas-skills)

### License/Terms of Use:

MIT

## Use Case:

External developers and media engineers use this skill to prepare Tencent Cloud MPS script commands for transcoding, enhancement, subtitle extraction or translation, media understanding, AIGC media generation, COS input and output handling, and task or usage queries.

### Deployment Geography for Use:

Global, subject to Tencent Cloud MPS regional availability and endpoint configuration.

## Known Risks and Mitigations:

Risk: The security review flags the release for review because it supports anti-detection video deduplication.

Mitigation: Avoid using the video dedupe feature for platform-detection bypass and review dedupe requests before execution.

Risk: Tencent Cloud MPS processing can create unintended cloud charges, especially for repeated submissions or high-cost media generation.

Mitigation: Use dry runs for uncertain or expensive operations, require explicit confirmation before processing tasks, and configure Tencent Cloud spending alerts or limits.

Risk: Credential handling and execution environment choices can expose Tencent Cloud credentials or broaden account impact.

Mitigation: Install in an isolated virtual environment, use least-privilege Tencent Cloud credentials, avoid running scripts from untrusted project directories, and do not collect user secrets in chat.

Risk: Unpinned dependencies and endpoint configuration can change runtime behavior or direct requests to the wrong service endpoint.

Mitigation: Pin dependencies before use and verify TENCENTCLOUD_MPS_ENDPOINT is one of Tencent's intended MPS endpoints.

## Reference(s):

- [Tencent MPS ClawHub skill page](https://clawhub.ai/tencent-mpaas-skills/skills/tencent-mps)
- [MPS best practices](references/best_practices.md)
- [MPS transcoding reference](references/mps_transcode.md)
- [MPS enhancement reference](references/mps_enhance.md)
- [MPS subtitles reference](references/mps_subtitle.md)
- [MPS image processing reference](references/mps_imageprocess.md)
- [MPS AIGC image reference](references/mps_aigc_image.md)
- [MPS AIGC video reference](references/mps_aigc_video.md)
- [MPS AIGC audio reference](references/mps_aigc_audio.md)
- [MPS COS operations reference](references/mps_cos_ops.md)
- [MPS task query reference](references/mps_query_task.md)
- [Tencent Cloud MPS pricing](https://cloud.tencent.com/document/product/862/36180)
- [Tencent Cloud MPS request structure and regions](https://cloud.tencent.com/document/product/862/37572)
- [Tencent Cloud ProcessMedia API](https://cloud.tencent.com/document/api/862/37578)
- [Tencent Cloud ProcessImage API](https://cloud.tencent.com/document/api/862/112896)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with inline shell commands, task identifiers, cost reminders, and output links when applicable.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target the bundled Tencent MPS Python scripts and may include dry-run or asynchronous execution flags.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter reports 1.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
