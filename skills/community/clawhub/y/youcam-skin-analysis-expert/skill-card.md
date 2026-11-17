## Description:

Analyzes a single selfie with YouCam AI and returns scores for selected skin conditions plus skin type in a readable report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youcam-api](https://clawhub.ai/user/youcam-api)

### License/Terms of Use:

MIT-0

## Use Case:

People seeking a cosmetic skin report can provide a selfie and receive scores for selected skin concerns and skin type, with brief guidance for understanding the results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected selfie is sent to YouCam/Perfect Corp for analysis.

Mitigation: Explain the upload and provider privacy terms before analysis, and proceed with the user's informed choice.

Risk: Analysis uses YouCam API credits.

Mitigation: Check the feature cost and tell the user the expected credit charge before running it.

Risk: API credentials and dependencies require care.

Mitigation: Protect the YOUCAM_API_KEY and use maintained dependency versions.

Risk: Cosmetic scores could be mistaken for a medical assessment.

Mitigation: Present results as reference only and include the required dermatologist disclaimer.

## Reference(s):

- [Perfect Corp AI Skin Analysis API documentation](https://docs.perfectcorp.com/reference/ai_skin_analysis.md)
- [Score interpretation](references/interpretation.md)
- [Report format and disclaimer](references/output-format.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Readable Markdown report with selected skin-condition scores, skin type, and result images when returned.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports returned ui_score values and does not present raw scores; available concerns depend on the user's selection.]

## Skill Version(s):

1.1.2 (source: frontmatter; server release 1.1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
