## Description:

Use when the user wants to generate a video through the superouter, especially the `seedance-2.0-v1` omni-reference workflow with ordered assets, async submission, `taskId` polling, and direct download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ningxiaoxiao](https://clawhub.ai/user/ningxiaoxiao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide video generation through the superouter platform API, including balance checks, ordered asset uploads, asynchronous task submission, status polling, and direct download URL retrieval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials, prompts, task metadata, and selected media may be sent to a fixed external service over plaintext HTTP.

Mitigation: Use only non-sensitive media and prompts, confirm whether the service supports HTTPS before sending data, and avoid using valuable or broad-scope API credentials.

Risk: A compromised or misused superouter client key could incur unwanted spending or expose account activity.

Mitigation: Use a dedicated low-privilege SUPER_KEY with spending limits, rotate it regularly, and stop if the platform returns authorization errors.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ningxiaoxiao/skills/superouter-video-gen)
- [superouter balance endpoint](http://superouter.nesports.top/me/balance)
- [superouter asset upload endpoint](http://superouter.nesports.top/v1/video/assets/upload)
- [superouter omni-reference task submit endpoint](http://superouter.nesports.top/v1/video/omni-reference/task/submit)
- [superouter omni-reference task query endpoint](http://superouter.nesports.top/v1/video/omni-reference/task/query)
- [superouter task list endpoint](http://superouter.nesports.top/me/tasks?limit=50)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request and response bodies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and SUPER_KEY; can send local media files, prompts, task metadata, and API credentials to the superouter service.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
