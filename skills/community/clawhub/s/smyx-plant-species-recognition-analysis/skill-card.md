## Description:

Identifies plant species from images or video and returns structured species, family, growth habit, care guidance, and report information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, researchers, and gardening users can submit plant media or URLs to identify species and receive structured plant knowledge. Agents can also retrieve prior cloud-hosted plant recognition reports for the resolved user identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plant photos, videos, URLs, and an internal user identifier are sent to lifeemergence.com for cloud analysis.

Mitigation: Use the skill only when cloud processing by that vendor is acceptable, and avoid submitting sensitive or unnecessary media.

Risk: The skill may create or reuse local identity data and cloud tokens in workspace data files.

Mitigation: Treat data/smyx-api-key.txt and data/smyx-common-claw.db as sensitive local files and do not store real phone numbers or secrets in the API key file.

Risk: Plant identification and care guidance may be incorrect or incomplete for high-consequence uses.

Mitigation: Use results as informational guidance and consult qualified experts before relying on them for edible, medicinal, safety, or ecological decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-plant-species-recognition-analysis)
- [Skill Demo](https://lifeemergence.com/sample.html)
- [API Interface Documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-like structured text with optional report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save analysis output to a user-specified file when requested.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
