## Description: <br>
Browse and search YTHT BBS boards, draft posts with context, and publish only after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yupoet](https://clawhub.ai/user/yupoet) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents assisting YTHT BBS users use this skill to read boards and threads, search before replying, draft posts with relevant context, and publish only after explicit user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The separate ytht-bbs plugin may handle forum authentication and posting permissions. <br>
Mitigation: Review the plugin and confirm account permissions before using this skill with a linked forum account. <br>
Risk: An agent could prepare an inaccurate or unintended forum post. <br>
Mitigation: Read or search relevant context first, prepare a draft, surface similar-thread warnings when present, and require user confirmation before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yupoet/ytht-bbs) <br>
- [Publisher profile](https://clawhub.ai/user/yupoet) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Guidance] <br>
**Output Format:** [Markdown and plugin tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Drafts are prepared before publishing, and publishing requires explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
