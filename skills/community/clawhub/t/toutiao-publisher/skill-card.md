## Description: <br>
Publish articles to Toutiao (Today's Headlines). Handles persistent authentication (login once) and session management. Opens browser for interactive publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guanyang](https://clawhub.ai/user/guanyang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to manage Toutiao login state and publish articles through the Toutiao publisher portal, including Markdown content and optional cover images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Saved browser sessions can allow reuse of a logged-in Toutiao publisher account. <br>
Mitigation: Review where browser state is stored, clear it when work is complete, and only install the skill when account reuse is intended. <br>
Risk: Automated publishing may post content without sufficiently clear final confirmation. <br>
Mitigation: Require the agent to show the title, content, cover image, and final publish action for explicit approval before any live publish. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guanyang/toutiao-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and browser publishing actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use saved browser session state and can publish to a live Toutiao account when directed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
