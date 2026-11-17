## Description:

TikTok Live stream monitoring and recording automation that uses Playwright visual detection and network traffic monitoring to capture FLV stream URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check whether TikTok profiles are live, extract stream URLs, and support recording or notifications when live status changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts TikTok, inspects network responses, invokes external media tools, and writes temporary output.

Mitigation: Run it in a constrained, low-privilege environment and review network, browser, and filesystem access before use.

Risk: The security guidance flags command construction, eval usage, and temporary-file handling as issues to fix before routine use.

Mitigation: Do not pass untrusted usernames or quality values; harden command construction, remove eval-based execution, and use safer temporary-file handling before routine operation.

Risk: The security summary notes underdocumented external tool execution and leftover-log risks.

Mitigation: Review and document required tools such as Playwright, streamlink, and yt-dlp, and clean or isolate generated logs after runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kikikari/skills/tiktok-live-mon)
- [Publisher profile](https://clawhub.ai/user/kikikari)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON status objects, stream URLs, and command-line output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke browser automation and external media tools, contact TikTok, and write temporary logs, screenshots, or stream output depending on the command used.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
