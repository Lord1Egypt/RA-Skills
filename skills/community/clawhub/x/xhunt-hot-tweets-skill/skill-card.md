## Description:

Extracts XHunt X/Twitter hot-tweet rankings and returns Chinese summaries, engagement data, source links, and short trend observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dotheworknow](https://clawhub.ai/user/dotheworknow)

### License/Terms of Use:


## Use Case:

External users and content analysts use this skill to request current XHunt hot-tweet lists filtered by region, time window, tag, and AI-product relevance. The skill formats each result with a tweet link, a Chinese one-line summary, engagement statistics, and concise observations for recap or repost workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may browse XHunt public ranking pages when asked broadly for hot posts or tweet summaries.

Mitigation: Use it only for intended XHunt trend-summary requests and review returned tweet links and engagement data before reuse.

Risk: Browser extraction or web-fetch fallback can be incomplete if XHunt is unavailable or its page structure changes.

Mitigation: Follow the skill behavior that marks degraded fetching, reports unavailable fields as NA, and returns an explicit failure instead of fabricating results.

Risk: The README installation example uses rsync with --delete, which removes files inside the target skill directory.

Mitigation: Confirm the destination path before running the install command.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dotheworknow/skills/xhunt-hot-tweets-skill)
- [XHunt trends](https://trends.xhunt.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style Chinese text with tweet links, one-line summaries, engagement statistics, and observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires live access to XHunt; missing data fields are reported as NA and fallback fetching may be incomplete.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter and changelog report 2.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
