## Description: <br>
Turn Weixin/Wechat replies into readable image cards by rendering HTML into long PNG screenshots for long direct-chat replies, visual cards, posters, charts, tables, timelines, diagrams, dashboards, or mixed text-image presentations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssochi](https://clawhub.ai/user/ssochi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert long Weixin or WeChat replies into readable PNG image cards. It is useful when chat-native text would be too long or when the response needs a polished HTML layout with tables, charts, diagrams, or mixed media. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rendering HTML that loads untrusted remote resources can expose the render environment to unwanted network content or tracking. <br>
Mitigation: Keep generated HTML self-contained when possible and avoid untrusted remote resources. <br>
Risk: Cleanup commands could remove the wrong files if paths are reused carelessly. <br>
Mitigation: Write generated files under /tmp or the workspace and delete only files created by the current render. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssochi/weixin-long-image) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and generated PNG image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Renders complete HTML into long PNG screenshots and may create temporary HTML files that should be cleaned up after successful sending.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
