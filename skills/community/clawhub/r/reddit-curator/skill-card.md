## Description: <br>
Curates and summarizes top Reddit posts from chosen subreddits, applies filters for relevance, and prepares a daily digest for delivery through configured channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[geoffguides](https://clawhub.ai/user/geoffguides) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to monitor selected Reddit communities, filter posts by engagement or keywords, and receive concise digests without manually browsing each subreddit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Reddit account credentials, including a password, which can grant account-level access if mishandled. <br>
Mitigation: Do not provide Reddit password access unless the implementation and credential storage are trusted; confirm credential handling before installation. <br>
Risk: The documentation conflicts on whether the skill is read-only while also describing saved-post syncing and other account-changing behavior. <br>
Mitigation: Confirm account-changing features such as saved-post syncing are disabled by default, opt-in, and visible to the user before execution. <br>
Risk: Scheduled delivery and stored configuration can continue sending digests or retaining preferences after the user expects the workflow to stop. <br>
Mitigation: Confirm how scheduled delivery is paused or stopped and where delivery settings, subreddit lists, and credentials are stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/geoffguides/reddit-curator) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [Reddit app preferences](https://www.reddit.com/prefs/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown digest text with links, summary bullets, and configuration guidance for subreddit, schedule, delivery, and filter settings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce delivery-ready digest content for Telegram, email, or Discord.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
