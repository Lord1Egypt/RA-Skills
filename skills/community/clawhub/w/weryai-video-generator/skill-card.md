## Description: <br>
Generate and transform WeryAI videos from text, images, storyboard frames, or first-frame and last-frame guidance, including bounded wait polling, status checks, model switching, and dry-run previews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weryai-developer](https://clawhub.ai/user/weryai-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate WeryAI videos from prompts or reference images, check model support, poll task status, and return playable video links when generation completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Most executable behavior depends on shared runtime core files that are outside the reviewed artifact. <br>
Mitigation: Install only if you trust the runtime core and WeryAI API endpoint; review the runtime core before production use. <br>
Risk: The skill uses WERYAI_API_KEY and can submit prompts or media to external WeryAI API hosts. <br>
Mitigation: Use a scoped API key when available, avoid sensitive media, and keep API base URL overrides limited to trusted destinations. <br>
Risk: Real generation commands can consume WeryAI credits. <br>
Mitigation: Use dry-run or model/status checks before paid submissions and confirm final parameters before creating a new task. <br>


## Reference(s): <br>
- [WeryAI Video Generator on ClawHub](https://clawhub.ai/weryai-developer/weryai-video-generator) <br>
- [WeryAI API keys](https://www.weryai.com/api/keys) <br>
- [WeryAI Video Generation Models](references/api-models.md) <br>
- [WeryAI Error Codes](references/error-codes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with playable video links and JSON command output from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include task IDs, batch IDs, task status, video URLs, request summaries, balance data, and error codes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
