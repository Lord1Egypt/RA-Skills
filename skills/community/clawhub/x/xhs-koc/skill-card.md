## Description:

Provides read-only Xiaohongshu (Rednote) search, creator, note, and comment data as structured JSON for research and creator evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and research teams use the skill to search public Xiaohongshu notes, review creator and engagement data, and summarize comment sentiment for content research and creator evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and note or creator links are sent to the third-party Guaikei API when a request runs.

Mitigation: Tell the user what query or link will be sent and avoid submitting sensitive material.

Risk: The security scan was partial, so its benign verdict does not mean every component was fully inspected.

Mitigation: Review the skill source before installation if the remaining unchecked code matters to your environment.

## Reference(s):

- [API provider](https://www.guaikei.com)
- [Output contract](references/contract.md)
- [Command options](references/options.md)
- [Setup and FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON response envelope with note, creator, engagement, or comment records as available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides success, empty-result, and error responses in a consistent envelope.]

## Skill Version(s):

1.2.3 (source: evidence.json release.version, SKILL.md frontmatter, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
