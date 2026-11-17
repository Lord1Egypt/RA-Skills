## Description:

Fetches and displays the latest edition from the SoulMD newsletter RSS feed, including title, date, link, and a brief excerpt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meastt](https://clawhub.ai/user/meastt)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to fetch the latest SoulMD newsletter entry from Buttondown RSS, report its title, date, link, subscription URL, and excerpt, and optionally detect whether a new edition has appeared since the last check.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Buttondown and displays content and links from the RSS feed.

Mitigation: Run it only where outbound access to Buttondown is expected, and review newsletter links before acting on them.

Risk: The new-edition check may write a small last-seen state file under ~/.openclaw.

Mitigation: Confirm local state-file writes are acceptable for the runtime, and remove the state file when tracking should be reset.

Risk: The packaged scripts/fetch_latest.py artifact is malformed and should not be executed as-is.

Mitigation: Repair or replace the packaged script before direct execution and review the intended Python behavior before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meastt/skills/soulmd-newsletter)
- [SoulMD RSS feed](https://buttondown.com/soulmd/rss)
- [SoulMD newsletter subscription page](https://buttondown.com/soulmd)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text with newsletter metadata, links, status messages, and excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact Buttondown RSS and, when checking for new editions, store last-seen state under ~/.openclaw.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
