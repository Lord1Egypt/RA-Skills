## Description:

Analyzes a local MP4 short-form video with StepFun vision and optional ASR models to produce a narrative viral-video deconstruction report covering topic, story, structure, events, audience insight, hook, pacing, and BGM cues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, operators, and content teams use this skill to turn Douyin or Xiaohongshu-style MP4 videos into structured narrative analysis for script writing, shot planning, topic selection, and remix planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected video and optional extracted audio transcript are sent to StepFun cloud services for analysis.

Mitigation: Use the skill only for videos whose cloud processing is acceptable, and review StepFun retention and deletion behavior before using private or sensitive media.

Risk: The quickstart evidence includes a concrete API key value, which should be treated as exposed.

Mitigation: Create a new StepFun API key, store it outside the package in a protected environment variable or secret store, and revoke any published key.

Risk: Cloud file cleanup is attempted after analysis, but cleanup success is not verified and uploads can be retained with --keep-upload.

Mitigation: Avoid --keep-upload unless needed, and verify deletion in the StepFun account when processing sensitive content.

Risk: The packaged artifact references templates/report.md.j2, but that template is not present in the artifact file list.

Mitigation: Confirm the report template is supplied before deployment or expect report rendering to fail at runtime.

Risk: BGM analysis is inferred from visual pacing and context rather than true music identification.

Mitigation: Treat BGM findings as heuristic and use a dedicated music-recognition service when exact track identification is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jack-yang-ai/skills/video-deconstruct)
- [Publisher profile: jack-yang-ai](https://clawhub.ai/user/jack-yang-ai)
- [Quickstart guide](guides/01-quickstart.md)
- [Narrative deconstruction guide](guides/02-叙事式拆解说明.md)
- [Prompt engineering guide](guides/03-prompt-engineering.md)
- [Sample output](examples/sample-output.md)
- [StepFun platform](https://platform.stepfun.com)
- [StepFun API base URL](https://api.stepfun.com/v1)

## Skill Output:

**Output Type(s):** [markdown, JSON, text]

**Output Format:** [Markdown report, JSON analysis file, and optional plain-text ASR transcript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes outputs under output/{video_stem}-report.md, output/{video_stem}-analysis.json, and, when ASR is enabled, output/{video_stem}-transcript.txt.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
