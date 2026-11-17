## Description:

Turn Weixin/Wechat replies into readable image cards by rendering HTML into long PNG screenshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssochi](https://clawhub.ai/user/ssochi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to convert long Weixin or WeChat replies into readable long-image article cards, posters, dashboards, or other HTML-based visual layouts for delivery in direct chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The HTML-to-image renderer can run active HTML with unrestricted browser networking.

Mitigation: Review HTML before rendering and avoid untrusted HTML, remote images, scripts, iframes, or sensitive content unless the renderer is isolated or updated to block network requests and JavaScript.

Risk: Temporary image or HTML outputs may contain sensitive user content.

Mitigation: Write outputs inside the workspace or /tmp and delete only artifacts created for the current render after the message is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssochi/skills/weixin-long-image)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance, image files]

**Output Format:** [Complete HTML rendered to a long PNG screenshot with a short send message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses daytime or dark WeChat-style article templates, writes outputs to an absolute path, and deletes temporary render artifacts after a successful send unless the user asks to keep them.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
