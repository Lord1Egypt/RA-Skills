## Description:

Turns a free-form product description into a 15-30 second AI-generated ad with hooks, a call to action, and visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and creators use this skill to turn pasted product descriptions or feature lists into short Revid ad videos with hook, benefit, call-to-action, caption, music, and visual settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product copy, brand notes, and provided media are sent to Revid for processing.

Mitigation: Use only content approved for Revid processing, and avoid confidential or regulated content unless that use has been approved.

Risk: The skill requires a Revid API key.

Mitigation: Store REVID_API_KEY in an approved secret store or environment, do not commit it, and rotate it if exposure is suspected.

Risk: The bundled polling example can run without an explicit timeout.

Mitigation: Use bounded polling, timeouts, and retry limits when adapting the example for automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/api00/skills/revid-product-description-to-ad)
- [Revid public render endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid public status endpoint](https://www.revid.ai/api/public/v3/status)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands for Revid API calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or retrieves a Revid video URL after render/status polling; requires REVID_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
