## Description: <br>
This skill helps agents prepare and invoke RunComfy CLI calls for ByteDance Seedance 2.0 Pro to generate 4-15 second 720p videos from prompts and optional image, video, or audio references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kalvinrv](https://clawhub.ai/user/kalvinrv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to generate short cinematic Seedance 2.0 Pro videos through RunComfy, including lip-synced spokesperson clips, multi-modal reference-guided scenes, and reproducible creative variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RunComfy account tokens are sensitive credentials. <br>
Mitigation: Keep RUNCOMFY_TOKEN private, use the RunComfy CLI login flow or configured token storage, and avoid exposing tokens in prompts, logs, or shared command history. <br>
Risk: Prompts and reference media may be uploaded to RunComfy for processing. <br>
Mitigation: Avoid sending private prompts or sensitive image, video, or audio references unless the user is comfortable sharing them with RunComfy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kalvinrv/seedance-v2) <br>
- [RunComfy](https://www.runcomfy.com) <br>
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2) <br>
- [Seedance 2.0 Pro model page](https://www.runcomfy.com/models/bytedance/seedance-v2/pro?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2) <br>
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=seedance-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides RunComfy CLI invocation; generated media is produced by the external RunComfy service.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
