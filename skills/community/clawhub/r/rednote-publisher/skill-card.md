## Description: <br>
Automates publishing long-form Xiaohongshu web posts by guiding browser setup, content entry, one-click formatting, publishing, and post-publication verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1122525](https://clawhub.ai/user/1122525) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Creators and operators use this skill to publish long-form or text-heavy Xiaohongshu notes through the web creator platform with repeatable browser actions, formatting checkpoints, and final verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent control of a logged-in Xiaohongshu creator account and can publish public content. <br>
Mitigation: Use a dedicated OpenClaw browser profile with no unrelated sessions, review the active account and full post preview yourself, and require explicit confirmation before publishing. <br>
Risk: The documented flow does not require a final human confirmation before clicking publish. <br>
Mitigation: Add a mandatory human approval checkpoint after preview review and before the agent activates the publish control. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1122525/rednote-publisher) <br>
- [Xiaohongshu creator publish page](https://creator.xiaohongshu.com/publish/publish?source=official) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Browser action steps] <br>
**Output Format:** [Markdown with inline JSON, bash, and browser action examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes checkpoint guidance for account state, editor state, preview review, publishing, and post status verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
