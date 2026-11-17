## Description:

Search personal video and photo libraries for clips, images, dialogue, people, and location-based footage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reelary](https://clawhub.ai/user/reelary)

### License/Terms of Use:

MIT-0

## Use Case:

External users can locate matching moments in their own video and photo libraries, including visual matches, transcript excerpts, recognized people, and geotagged footage; some search features require Reelary Pro.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search results and requested previews may reach the user's AI provider despite local processing.

Mitigation: Choose which media folders to index and consider provider exposure before requesting previews or sharing search results.

Risk: The CLI invocation uses an unpinned software dependency.

Mitigation: Prefer a verified, preinstalled or version-pinned Reelary CLI, and review the separately linked setup skill before installation or indexing.

## Reference(s):

- [Reelary agent guidance](https://reelary.app/agents)
- [Find Footage on ClawHub](https://clawhub.ai/reelary/skills/reelary-find-footage)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Concise text or Markdown lists with media paths, timestamps, match summaries, and transcript excerpts when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results can include full file paths and exact clip start and end times.]

## Skill Version(s):

0.1.0 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
