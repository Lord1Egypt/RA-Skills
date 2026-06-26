## Description: <br>
Reviews watchOS code for app lifecycle, complications (ClockKit/WidgetKit), WatchConnectivity, and performance constraints. Use when reviewing code with import WatchKit, WKExtension, WKApplicationDelegate, WCSession, or watchOS-specific patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review watchOS Swift and SwiftUI code for lifecycle, WidgetKit or ClockKit complications, WatchConnectivity, and performance issues before reporting file-line findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes an under-scoped file-protection recommendation around `.noFileProtection` for background access. <br>
Mitigation: Do not apply `.noFileProtection` to health, personal, credential, financial, or other sensitive data; use the least permissive protection class compatible with the required background behavior. <br>
Risk: watchOS findings can be misleading if lifecycle, background-mode, complication, or WatchConnectivity claims are made without checking the relevant project artifacts. <br>
Mitigation: Require file-line evidence, full surrounding-unit review, and concrete artifacts such as Info.plist, entitlements, target capabilities, or call-order source before reporting; otherwise downgrade the item to a review question. <br>


## Reference(s): <br>
- [WatchKit App Lifecycle](references/lifecycle.md) <br>
- [watchOS Complications](references/complications.md) <br>
- [WatchConnectivity](references/connectivity.md) <br>
- [watchOS Performance](references/performance.md) <br>
- [ClawHub skill page](https://clawhub.ai/anderskev/watchos-code-review) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown issue review with [FILE:LINE] ISSUE_TITLE findings and review questions when evidence is insufficient] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings require file-line locations, surrounding-unit review, and watchOS-specific artifact checks before reporting.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
