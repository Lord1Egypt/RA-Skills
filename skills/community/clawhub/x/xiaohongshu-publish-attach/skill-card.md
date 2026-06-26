## Description: <br>
Auto-publishes Xiaohongshu long-form notes on Linux by attaching to a Chrome/VNC session and running the bundled publish script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m-lemon](https://clawhub.ai/user/m-lemon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to prepare and publish Xiaohongshu long-form posts from a Linux/VNC environment with an authenticated Chrome creator session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish live Xiaohongshu content through a logged-in account. <br>
Mitigation: Run without --submit for review or dry-run first, then use --submit only when the post is intended for publication. <br>
Risk: The skill uses a shared logged-in Chrome profile, which can expose account context across automations. <br>
Mitigation: Use a dedicated Chrome profile or account instead of the shared Zhihu profile when isolating publication workflows matters. <br>
Risk: The fallback path can perform desktop-level clicks in a VNC session. <br>
Mitigation: Set XHS_DISABLE_SCREEN_CLICK=1 unless screen clicking is needed, and verify browser permissions and screenshots after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m-lemon/xiaohongshu-publish-attach) <br>
- [Linux + VNC setup](references/linux-vnc-setup.md) <br>
- [Shared Chrome with zhihu-publish-attach](references/shared-chrome-with-zhihu.md) <br>
- [Xiaohongshu Creator Center](https://creator.xiaohongshu.com) <br>
- [Google Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash commands; runtime can return JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Linux, Python, Chrome remote debugging/VNC, Selenium, chromedriver, and a logged-in Xiaohongshu Creator Center session.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
