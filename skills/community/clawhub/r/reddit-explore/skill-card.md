## Description:

Searches Reddit posts for a requested topic through Apify and helps an agent summarize community sentiment, key themes, and notable discussions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netmsglog](https://clawhub.ai/user/netmsglog)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Reddit discussions on a topic, gather Apify-backed post data, and produce concise summaries of community sentiment, themes, and notable posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reddit search topics are sent to Apify and may be processed by that third-party service.

Mitigation: Use the skill only for topics appropriate to share with Apify and avoid sending sensitive search terms.

Risk: The Apify API token grants account access and can consume platform credits.

Mitigation: Set APIFY_TOKEN through a protected environment or secret manager and avoid passing tokens on the command line.

Risk: The required apify-client package is installed into the local Python environment.

Mitigation: Install apify-client in a virtual environment with pinned versions when deploying the skill.

## Reference(s):

- [Apify Setup Guide](references/apify-setup.md)
- [Apify Console](https://console.apify.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summary with Reddit post links and JSON-backed findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, apify-client, and APIFY_TOKEN; the default search limit is 30 posts.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
