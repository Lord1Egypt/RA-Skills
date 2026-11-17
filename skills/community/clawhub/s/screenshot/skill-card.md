## Description:

Capture, inspect, and compare screenshots of screens, windows, regions, web pages, simulators, and CI runs with the right tool, wait strategy, viewport, and output format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and documentation authors use this skill to choose capture tooling and stabilize screenshot workflows for debugging, testing, documentation, bug reports, and visual comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Screenshots can expose secrets, internal URLs, personal data, notifications, or other sensitive visible content.

Mitigation: Review captures before sharing and mask, avoid, or remove sensitive regions when they are not the subject of the screenshot.

Risk: Unstable UI state, animations, timestamps, cursor blinks, or changing viewport settings can make screenshot evidence misleading.

Mitigation: Wait for the target state, fix viewport and theme settings, disable or avoid noisy UI, and compare before/after screenshots under the same conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/screenshot)
- [Skill homepage](https://clawic.com/skills/screenshot)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers desktop, browser, simulator, CI, and visual-diff screenshot workflows.]

## Skill Version(s):

1.0.1 (source: server evidence release.version and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
