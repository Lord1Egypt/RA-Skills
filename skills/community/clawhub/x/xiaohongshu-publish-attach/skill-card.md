## Description:

Automates Xiaohongshu long-form publishing on Linux by attaching to a logged-in Chrome/VNC session and running the provided publish script with title, body, tags, and optional submit behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m-lemon](https://clawhub.ai/user/m-lemon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to publish long-form Xiaohongshu creator-center posts from a Linux/VNC environment through an existing Chrome session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a persistent logged-in Chrome profile that may contain Xiaohongshu and Zhihu sessions.

Mitigation: Use a dedicated Chrome profile for automation and close the debug Chrome session when publishing is complete.

Risk: Using --submit performs a real Xiaohongshu post.

Mitigation: Review generated content first and run without --submit when a dry run is needed.

Risk: The optional pyautogui fallback can perform screen-level clicks in the VNC session.

Mitigation: Disable the fallback with XHS_DISABLE_SCREEN_CLICK=1 unless screen-click recovery is explicitly needed.

Risk: Running browser automation with elevated privileges increases the impact of mistakes or compromise.

Mitigation: Run the skill as a normal user and avoid sudo or root execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m-lemon/skills/xiaohongshu-publish-attach)
- [Linux + VNC setup](references/linux-vnc-setup.md)
- [Shared Chrome with zhihu-publish-attach](references/shared-chrome-with-zhihu.md)
- [Xiaohongshu creator center](https://creator.xiaohongshu.com)
- [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Linux, Chrome remote debugging, Selenium, chromedriver, and a logged-in Chrome profile.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
