## Description:

Automation for TikTok Live shopping, including monitoring pinned products, adding to cart, and preparing for checkout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kritsanan1](https://clawhub.ai/user/kritsanan1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to monitor TikTok Live streams for pinned products, collect cart data, and prepare checkout steps while retaining manual final purchase confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is framed as TikTok shopping automation, while the authoritative security summary says the shipped code is mostly simulation and still points users toward real account, cart, checkout, and unofficial dependency use.

Mitigation: Review before installing; treat it as a prototype or simulator unless the publisher clearly separates simulation from production use and documents exact browser and account permissions.

Risk: Optional Selenium, ChromeDriver, and unofficial TikTokLive dependency use may affect browser sessions and account activity.

Mitigation: Pin and verify dependencies, use an isolated browser profile, and keep final checkout or purchase confirmation manual.

## Reference(s):

- [ChromeDriver](https://chromedriver.chromium.org/)
- [ClawHub skill page](https://clawhub.ai/kritsanan1/skills/tiktok-live-cart-automation)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands; scripts emit console logs and JSON files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a TikTok username and supports optional duration and headless-mode parameters; final checkout confirmation remains manual.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
