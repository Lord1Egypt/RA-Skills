## Description:

Retrieves real-time TikTok video comments by video ID using Qinghu AI's comment lookup tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving TikTok analysts and creators can retrieve a video's comments by video ID and summarize the conversation or provide the returned records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to install or upgrade Node and qhkit, changing the host environment.

Mitigation: Prefer a preinstalled, pinned qhkit version and approve environment changes before installation.

Risk: A Qinghu API token is needed on the host for authenticated retrieval.

Mitigation: Use platform-managed secrets and avoid exposing the token in commands or outputs.

Risk: Comment retrieval is paid, and charges can rise with the number of results or calls.

Mitigation: Estimate credits and confirm the expected cost and scope with the user before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-tiktok-video-comments)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON files]

**Output Format:** [Markdown summary with comment data or a path to a JSON results file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a brief preview, pagination details, and credits spent.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
