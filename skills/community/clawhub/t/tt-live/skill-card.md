## Description:

TikTok LIVE monitor. Check whether a TikTok user is live right now, resolve their current m3u8 stream URL, or spawn a background daemon that polls them over a timer window and emits go_live / go_offline / rename_detected events for the sub-agent to announce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to check a TikTok user's LIVE status, resolve the current m3u8 stream URL, or monitor one user over a defined time window and consume structured live, offline, and rename events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unvalidated TikTok handles in shell workflows can create command-injection exposure.

Mitigation: Validate handles before use, pass each handle as a single quoted command argument, and avoid untrusted or free-form handles until validation is fixed.

Risk: The skill contacts TikTok and writes local monitor state, logs, and cached stream URLs.

Mitigation: Use an appropriate workspace location, review generated files for sensitive stream URLs, and remove cached state when monitoring is no longer needed.

Risk: Stream URLs are tied to live sessions and can become stale when a user goes offline and later starts a new live session.

Mitigation: Resolve a fresh URL for each active live session and treat cached URLs as records rather than durable playable links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kikikari/skills/tt-live)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON records, key=value daemon status lines, and line-oriented event logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local monitor state, logs, identity records, cached stream URLs, and daemon event files under the configured workspace.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata; artifact frontmatter states 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
