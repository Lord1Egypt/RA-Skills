## Description:

Monitors Twitter/X feeds with AI signal detection. Searches tweets semantically, manages signal detectors, and organizes curated tweets into bookmark folders. Use when the user wants to browse their Twitter feed, find tweets about a topic, set up content monitoring, or organize bookmarks. Do NOT use for general Twitter browsing without a Purefeed account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[poloniki](https://clawhub.ai/user/poloniki)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Purefeed account can search and monitor Twitter/X topics through semantic feed search and AI signal matches, manage signal detectors, and organize curated tweets in bookmark folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API error responses may include action hints that could redirect the agent based on externally supplied text.

Mitigation: Review API error hints before acting; check that any suggested action is relevant to the user's request and consult the linked API documentation when needed.

## Reference(s):

- [Purefeed API](https://purefeed.ai/api/v1)
- [Purefeed API change notes](https://purefeed.ai/llms.txt)
- [Purefeed API key setup](https://purefeed.ai/profile)
- [Purefeed on ClawHub](https://clawhub.ai/poloniki/skills/purefeed)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with clickable tweet and profile links, view counts, and concise summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tweet data is sorted by views or engagement unless the user requests otherwise.]

## Skill Version(s):

0.19.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
