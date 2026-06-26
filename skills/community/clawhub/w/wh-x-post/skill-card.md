## Description: <br>
Helps an agent post tweets, reply to tweets, quote tweets, and check Twitter/X login status through twitter-cli after user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baiyea](https://clawhub.ai/user/baiyea) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users can use this skill to prepare and publish Twitter/X posts, replies, and quote tweets with optional images. It is suited for workflows where the user reviews the text, target tweet ID, and attachments before the agent runs the posting command. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public Twitter/X content from the user's account through explicit script actions. <br>
Mitigation: Review the exact post, reply, quote target, tweet ID, and image paths before confirming any command. <br>
Risk: The commands rely on the user's logged-in browser session and twitter-cli installation. <br>
Mitigation: Check login status first when needed and install or configure twitter-cli only in an environment where using that account is intended. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may return tweet IDs, tweet URLs, login status, or structured error details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
