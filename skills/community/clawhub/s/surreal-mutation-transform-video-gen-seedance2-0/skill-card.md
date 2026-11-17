## Description:

Generates surreal short videos with WeryAI Seedance 2.0 from text prompts or a single input image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to expand short creative briefs into surreal production prompts, submit text-to-video or image-to-video jobs to WeryAI Seedance 2.0, and return playable video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image parameters can cause readable local files to be uploaded to WeryAI when local paths are supplied.

Mitigation: Prefer public HTTPS image URLs, reject untrusted image paths, and require explicit operator consent before any local file upload.

Risk: Generation uses a paid WeryAI API key and repeated runs can consume credits.

Mitigation: Run in an isolated environment with a WeryAI key intended for this use, confirm parameters before submission, and avoid automatic retries that create new jobs.

Risk: The bundled script does not enforce every skill-level model and parameter limit.

Mitigation: Validate model, duration, aspect ratio, resolution, audio, and unsupported fields against the skill documentation before invoking the script.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/surreal-mutation-transform-video-gen-seedance2-0)
- [WERYAI_VIDEO_API.md](resources/WERYAI_VIDEO_API.md)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI model and upload API host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and playable video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY and Node.js 18+; uses paid network calls and returns WeryAI task status or video URLs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
