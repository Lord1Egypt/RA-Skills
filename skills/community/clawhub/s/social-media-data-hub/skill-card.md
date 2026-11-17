## Description:

Unified Apify-based retrieval for TikTok, Instagram, X/Twitter, and YouTube profile, post, and comment data with cross-platform normalization for analysis workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[galaxy-earth](https://clawhub.ai/user/galaxy-earth)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve public social-media profiles, posts, single posts, and comment data across supported platforms, then normalize the results into shared JSON schemas for analysis workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify actor runs use a billing API token and may incur charges or expose credentials if token handling is not tightened.

Mitigation: Review before installing, use a least-privilege Apify token with spending limits, and prefer Authorization-header authentication over query-string tokens.

Risk: Weak URL and count controls can send unintended targets or unexpectedly large jobs to external actor runs.

Mitigation: Validate supported platform URLs, enforce count limits, reject unknown actor IDs, and avoid sensitive or private URLs and usernames.

Risk: Social-media retrieval relies on third-party Apify actors that process requested profile, post, and comment targets.

Mitigation: Make the third-party data-processing notice explicit and use the skill only with data sources permitted by organizational policy and applicable platform terms.

## Reference(s):

- [Apify Actor Quick Reference](references/apify_actors_reference.md)
- [ClawHub Skill Page](https://clawhub.ai/galaxy-earth/skills/social-media-data-hub)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown usage guidance with Python command examples and JSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and APIFY_TOKEN; fetch scripts return normalized JSON for profiles, posts, and comments where supported.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
