## Description:

Use the ClawRSS OpenClaw plugin to manage RSS feeds, persist web results, pull saved items, work with digest articles, and send Apple push notifications after the plugin is installed and enabled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ipocket-app](https://clawhub.ai/user/ipocket-app)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to operate ClawRSS feeds, saved web or article records, digest records, and push notifications within a workspace. It is intended for workflows that need consistent workspace scoping and verification after RSS, digest, or notification actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the wrong workspace ID can save items, mark cursors, change feeds, or send notifications in the wrong ClawRSS workspace.

Mitigation: Confirm or infer the correct workspace ID before write actions, and reuse it consistently as the namespace and consumer where required.

Risk: A normal website URL may be mistaken for an RSS or Atom feed URL.

Mitigation: Confirm the real RSS or Atom feed URL before subscribing, and report that the site was not subscribed when no feed URL is verified.

Risk: Push notification delivery may be assumed before push is configured.

Mitigation: Check push status when configuration is uncertain and report success only when the relevant ClawRSS push operation confirms it.

## Reference(s):

- [Use ClawRSS ClawHub page](https://clawhub.ai/ipocket-app/skills/use-clawrss)

## Skill Output:

**Output Type(s):** [Guidance, Text, API calls]

**Output Format:** [Markdown response summarizing tool calls, saved or updated items, verification status, and any missing user input]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the ClawRSS plugin to be installed and enabled, and uses the current workspace ID as the namespace for ClawRSS operations.]

## Skill Version(s):

2026.3.29 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
