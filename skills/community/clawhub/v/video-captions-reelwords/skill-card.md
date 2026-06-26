## Description: <br>
Generate captions for short-form videos using the ReelWords Caption API, including caption-job creation, status polling, and rendered-video download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Kmasterrr](https://clawhub.ai/user/Kmasterrr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, creators, and agent operators use this skill to submit short-form videos to ReelWords for stylized caption rendering, monitor the caption job, and retrieve the captioned video. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video URLs and submitted media are sent to ReelWords for processing. <br>
Mitigation: Use the skill only with videos or URLs that are appropriate to share with ReelWords. <br>
Risk: The ReelWords API key could be exposed if pasted into public chats, committed to source control, or passed through visible command history. <br>
Mitigation: Store REELWORDS_API_KEY in a private environment or runtime configuration and rotate it if exposure is suspected. <br>
Risk: The helper writes the rendered video to the output path provided by the caller. <br>
Mitigation: Choose output paths intentionally and avoid overwriting important files. <br>
Risk: API usage may consume ReelWords credits or hit usage limits. <br>
Mitigation: Review ReelWords API usage and handle HTTP 402 usage-limit responses before retrying. <br>


## Reference(s): <br>
- [ReelWords Caption API reference](references/api.md) <br>
- [ReelWords website](https://reelwords.ai) <br>
- [ReelWords Caption API base URL](https://api.reelwords.ai) <br>
- [ClawHub skill page](https://clawhub.ai/Kmasterrr/video-captions-reelwords) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/Kmasterrr) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON, files] <br>
**Output Format:** [Markdown guidance with shell commands, REST examples, JSON payloads, and an optional downloaded video file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and REELWORDS_API_KEY; the helper can print final job JSON and write the rendered video to a caller-provided output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
