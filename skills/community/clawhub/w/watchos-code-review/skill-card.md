## Description:

Reviews watchOS code for app lifecycle, complications (ClockKit/WidgetKit), WatchConnectivity, and performance constraints. Use when reviewing code with import WatchKit, WKExtension, WKApplicationDelegate, WCSession, or watchOS-specific patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review watchOS applications for lifecycle handling, complications and widgets, WatchConnectivity behavior, and device performance constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security review output depends on an unbundled external review protocol, which may affect whether findings are reported.

Mitigation: Vendor or remove the external protocol dependency before relying on the skill for security review.

Risk: Background file guidance may encourage disabling file protection too broadly.

Mitigation: Limit .noFileProtection guidance to explicitly non-sensitive data and document the tradeoff.

## Reference(s):

- [Watchos Code Review skill page](https://clawhub.ai/anderskev/skills/watchos-code-review)
- [watchOS Complications](references/complications.md)
- [WatchConnectivity](references/connectivity.md)
- [WatchKit App Lifecycle](references/lifecycle.md)
- [watchOS Performance](references/performance.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Guidance]

**Output Format:** [Markdown review findings using [FILE:LINE] ISSUE_TITLE entries and review questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings require concrete file locations, surrounding-scope review, and watchOS-specific supporting artifacts when applicable.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
