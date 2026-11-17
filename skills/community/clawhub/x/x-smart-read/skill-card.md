## Description:

Personal X (Twitter) analytics for timeline engagement, mentions, follower tracking, tweet and thread reading, bookmarks, and combined briefings via X API v2 with local caching and daily budget guards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nevaaron](https://clawhub.ai/user/nevaaron)

### License/Terms of Use:

Apache-2.0

## Use Case:

External users and developers use this skill to give an AI agent controlled read access to X account activity, public tweets, mentions, bookmarks, follower metrics, and daily or weekly social media briefings while tracking estimated API spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup handles X API credentials and stores them in a local config file.

Mitigation: Run setup only in a private terminal, verify the config file permissions, and grant the X app only the minimum read and bookmark permissions needed.

Risk: The skill runs Python scripts through uv and installs dependencies at execution time.

Mitigation: Install uv from a verified source and consider pinning dependencies or adding a reviewed lockfile before routine use.

Risk: Commands can spend real X API credits when they fetch fresh data or paginate.

Mitigation: Use dry-run, cache-backed commands, daily budget guards, and explicit user approval before expensive context, thread, lookup, or refresh operations.

## Reference(s):

- [X API v2 Quick Reference](artifact/references/x-api-quickref.md)
- [X Developer Platform](https://developer.x.com)
- [uv Python package runner](https://astral.sh/uv)
- [ClawHub skill listing](https://clawhub.ai/nevaaron/skills/x-smart-read)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text command output with analytics summaries, tweet links, error states, estimated API cost, and current daily spend.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON stores for cached tweets, mentions, bookmarks, follower history, and usage totals; supports dry-run and budget modes.]

## Skill Version(s):

2.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
