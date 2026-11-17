## Description:

V2EX Hot Topics Monitor helps agents answer requests about V2EX trending posts, technical discussions, digital life topics, and node-filtered community activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to request summaries of V2EX hot topics, node-specific discussions, reply counts, and active community posts. Review freshness before relying on the results because the release evidence reports fixed mock output rather than confirmed live V2EX fetching.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advertises live V2EX monitoring while the security evidence reports fixed mock topics, which can mislead users about freshness and provenance.

Mitigation: Verify live fetching behavior before relying on current V2EX data, or clearly disclose the output as mock or demonstration data.

Risk: No license identifier was provided in the server evidence or artifact files.

Mitigation: Confirm terms of use with the publisher before redistribution or commercial deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guohongbin-git/skills/v2ex-hot-cn)
- [Publisher profile](https://clawhub.ai/user/guohongbin-git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown or JSON-style topic lists with titles, nodes, reply counts, authors, and optional command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and curl according to release metadata; script output may be mock data.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
