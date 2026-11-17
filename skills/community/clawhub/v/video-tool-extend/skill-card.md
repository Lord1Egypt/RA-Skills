## Description:

Extend or continue an existing HTTPS video with a prompt via WeryAI (video-extend).

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to extend an existing public HTTPS video with a prompt, selected style, resolution, and duration through WeryAI. It is not intended for text-to-video generation from scratch or local file upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid WeryAI requests are not idempotent and may consume credits when submitted.

Mitigation: Use dry-run first and require explicit user confirmation of the video URL, prompt, duration, style, and resolution before submit or wait.

Risk: The provided public video URL, prompt, and WERYAI_API_KEY are sent to WeryAI for generation.

Mitigation: Install and run only if the user is comfortable sharing those inputs with WeryAI, and keep WERYAI_API_KEY in the runtime environment rather than files.

Risk: This skill only covers the video-extend workflow and does not upload local files or run sibling video CLIs.

Mitigation: Run only artifact/scripts/video_extend.js for this skill and verify the package contains only SKILL.md, eval.yaml, and scripts/video_extend.js before use.

## Reference(s):

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/video-tool-extend)
- [Publisher profile](https://clawhub.ai/user/zoucdr)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON CLI output and final video URLs as Markdown links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, WERYAI_API_KEY, paid network access to WeryAI, and a public HTTPS video URL.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
