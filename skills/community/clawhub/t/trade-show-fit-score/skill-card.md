## Description:

Scores a specific trade show against a company profile using Lensmor to support exhibit, attend, or skip decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

B2B trade show planning teams use this skill to retrieve a Lensmor fit score for one event, preserve the returned dimensions, and decide whether to exhibit, attend, or skip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Lensmor API key and sends event names or event IDs to Lensmor's platform.

Mitigation: Use only with an authorized Lensmor account and avoid submitting sensitive event planning information that should not be shared with Lensmor.

Risk: The fit score is limited to the API-returned score and dimensions and is not a complete exhibit ROI model.

Mitigation: Present the score as a profile signal, avoid inventing missing dimensions, and use additional event research or budget planning before committing spend.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weilun88313/skills/trade-show-fit-score)
- [Lensmor API documentation](https://api.lensmor.com/)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=trade-show-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LENSMOR_API_KEY; scores and breakdowns must come directly from the Lensmor API.]

## Skill Version(s):

1.2.1 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
