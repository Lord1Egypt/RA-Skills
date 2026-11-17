## Description:

Generate stylized captions for short-form videos using the ReelWords Caption API, including caption-job creation, status polling, and rendered-video download guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmasterrr](https://clawhub.ai/user/kmasterrr)

### License/Terms of Use:


## Use Case:

External creators, marketers, and developers use this skill to generate captioned short-form videos through ReelWords, tune caption styling, poll job status, and retrieve rendered outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The fallback video download path may expose the ReelWords API key during redirects.

Mitigation: Prefer result.downloadUrl downloads, avoid the video-endpoint fallback until redirects are handled without forwarding x-api-key, and rotate the key if exposure is suspected.

Risk: Captioning sends source video content to ReelWords for processing.

Mitigation: Use only videos that are acceptable to share with ReelWords, and avoid sensitive or private videos unless that transfer is approved.

## Reference(s):

- [ReelWords Caption API minimal reference](references/api.md)
- [ReelWords service](https://reelwords.ai)
- [ClawHub skill page](https://clawhub.ai/kmasterrr/skills/video-captions-reelwords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, bash, curl, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ReelWords caption job JSON and downloaded video files when the helper script is run with valid credentials.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
