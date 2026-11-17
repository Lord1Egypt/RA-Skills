## Description:

Xhsfenxi Pro collects Xiaohongshu account and note data through a local browser session, analyzes creator patterns and viral-topic formulas, and produces structured reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and creator-operations teams use this skill to gather Xiaohongshu public account content with a logged-in local browser session, classify creator archetypes, reverse-engineer high-performing content patterns, and generate reusable topic formulas and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a local Xiaohongshu session cookie and browser automation against that account.

Mitigation: Use only an account/session you are comfortable automating, keep the cookie file local, restrict file sharing, and delete or refresh the cookie when access is no longer needed.

Risk: The evidence security summary flags under-disclosed account-writing and self-promotion behavior, including a comment-posting function and optional ClawHub star action.

Mitigation: Do not expose or run account-mutating actions unless the user explicitly requests them after reviewing the command or function being invoked.

Risk: The skill documentation includes optional heartbeat, auto-update, and webhook push flows that can create persistence or external notifications.

Mitigation: Leave schedulers and webhook integrations disabled by default, review any cron or webhook configuration before enabling it, and remove those configurations during uninstall.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/xhsfenxi-pro)
- [README](artifact/README.md)
- [Full analysis workflow](artifact/workflow.md)
- [Xhsfenxi v2 workflow](artifact/workflow-xhsfenxi-v2.md)
- [Report templates](artifact/templates.md)
- [hsword frameworks](artifact/hsword-frameworks.md)
- [Migration toolkit](artifact/migration-toolkit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown reports, Python and shell snippets, JSON data files, and DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local analysis data and report files under the skill directory or /tmp when the user runs the documented workflows.]

## Skill Version(s):

2.1.4 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
