## Description:

A macOS browser automation skill that opens a requested website in the default browser from a site name, complete URL, or partial URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[strike163163](https://clawhub.ai/user/strike163163)

### License/Terms of Use:


## Use Case:

Developers and macOS users can use this skill to let an agent open recognized website names, complete URLs, or partial URLs in the local default browser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill opens URLs supplied by the user or agent, which may navigate to unwanted or untrusted sites.

Mitigation: Use it like a browser shortcut and only open links that the user requested or recognizes.

Risk: Browser selection is environment-dependent because the script opens the system default browser.

Mitigation: Do not rely on this skill to choose Safari or Chrome specifically; verify the local default browser when that matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/strike163163/skills/strike163163-my-browser-control)
- [Publisher profile](https://clawhub.ai/user/strike163163)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON status object and browser open action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local browser-capable macOS environment; user-provided site names may be mapped to predefined URLs or normalized with an https prefix.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
