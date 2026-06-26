## Description: <br>
Launches Chromium in non-headless mode inside a fixed 1200x720x24 Xvfb virtual display and lets an agent automate it with PyAutoGUI mouse, keyboard, screenshot, image matching, pixel, and window-focus operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[NHZallen](https://clawhub.ai/user/NHZallen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to run browser workflows that need a visible Chromium GUI in an isolated virtual display, including clicking, typing, scrolling, taking screenshots, finding images, and reading pixels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad live-browser control through mouse, keyboard, scrolling, and window-focus operations. <br>
Mitigation: Run it only in an isolated container or VM with a dedicated browser profile, and require human confirmation before posting, messaging, purchasing, changing settings, or deleting data. <br>
Risk: Screenshots and pixel reads can expose sensitive page content, including account data or private browsing context. <br>
Mitigation: Avoid personal accounts and treat screenshot outputs as sensitive data with restricted retention and sharing. <br>
Risk: Browser and Xvfb processes can remain active if the lifecycle is not closed. <br>
Mitigation: Call browser_stop after each workflow and monitor process cleanup in the runtime environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/NHZallen/virtual-desktop-browser) <br>
- [Publisher Profile](https://clawhub.ai/user/NHZallen) <br>
- [English Documentation](artifact/docs/en.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Images, Shell commands, Guidance] <br>
**Output Format:** [JSON dictionaries; screenshots are returned as Base64 PNG strings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Browser state persists across calls until browser_stop is invoked; the virtual display uses a fixed 1200x720x24 resolution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
