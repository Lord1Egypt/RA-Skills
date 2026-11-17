## Description:

Launches Chromium in non-headless mode inside a fixed 1200x720x24 Xvfb virtual display and automates mouse, keyboard, scrolling, screenshots, image matching, and window focus through PyAutoGUI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nhzallen](https://clawhub.ai/user/nhzallen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run GUI browser workflows inside an Xvfb display when non-headless Chromium and human-like mouse or keyboard interactions are needed, including pages that resist headless automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate clicks, typing, and screenshots in a real browser session, which may expose private data or violate site rules.

Mitigation: Use it only in an isolated disposable environment with a dedicated browser profile and avoid accounts, pages, or services where this automation is not permitted.

Risk: The browser launch disables Chromium sandboxing.

Mitigation: Run the skill under a non-privileged account inside a hardened container or VM, and avoid using Chromium with --no-sandbox unless those controls are in place.

Risk: Unpinned Python and system dependencies can change behavior between installations.

Mitigation: Pin the source and dependency versions before deployment and scan the resolved environment before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nhzallen/skills/virtual-desktop-browser)
- [README](README.md)
- [English Documentation](docs/en.md)
- [Spanish Documentation](docs/es.md)
- [Arabic Documentation](docs/ar.md)

## Skill Output:

**Output Type(s):** [JSON, Images, Shell commands, Configuration, Guidance]

**Output Format:** [JSON dictionaries; screenshots are Base64-encoded PNGs when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser lifecycle is manual: start the browser, perform actions, then stop it.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
