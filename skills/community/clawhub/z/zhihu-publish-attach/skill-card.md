## Description: <br>
Auto-publish Zhihu column articles on Linux by attaching to a Chrome session over VNC and running zhihu_publish.sh with agent-supplied title and body content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-lemon](https://clawhub.ai/user/m-lemon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an OpenClaw agent draft or accept Zhihu article content, open the Zhihu column editor in a logged-in Linux Chrome/VNC session, and publish or draft the post. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically publish real Zhihu column articles from a logged-in Chrome profile without a fresh confirmation step. <br>
Mitigation: Use explicit preview or draft wording when the user is not ready to post, omit --submit for drafts, and consider requiring confirmation before real publication. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/m-lemon/zhihu-publish-attach) <br>
- [Linux server + VNC setup](references/linux-vnc-setup.md) <br>
- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown or plain text article content, shell command invocations, and JSON publish/check results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux, python3, curl, unzip, Selenium, matching Chrome and chromedriver, VNC access, and a logged-in Zhihu Chrome profile.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
