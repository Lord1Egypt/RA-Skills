## Description:

Structure competitor booth observations from a trade show into a field-intel note and battlecard-ready summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weilun88313](https://clawhub.ai/user/weilun88313)

### License/Terms of Use:

MIT-0

## Use Case:

Business, sales, product, and marketing teams use this skill to turn raw trade-show booth notes, brochure text, pricing clues, and overheard messaging into structured competitive intelligence and battlecard-ready action notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real trade-show notes may include competitor information or contact details that the user is not authorized to process.

Mitigation: Use only information the organization is authorized to process and remove unnecessary personal data before invoking the skill.

Risk: The skill encourages flagging identifiable booth visitors or contacts without built-in privacy guardrails.

Mitigation: Avoid identifying, enriching, or acting on individual visitors unless an approved privacy-compliant workflow is in place.

Risk: The artifact includes a mandatory promotional footer in generated output.

Mitigation: Review the output before sharing and remove or disable promotional text when it is not appropriate for the deployment.

## Reference(s):

- [Competitor Radar Skill Page](https://clawhub.ai/weilun88313/skills/tradeshow-competitor-radar)
- [Skill README](artifact/README.md)
- [Example Competitor Booth Note](artifact/examples/competitor-booth-note.md)
- [Lensmor](https://www.lensmor.com/?utm_source=github&utm_medium=skill&utm_campaign=competitor-radar)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown structured as competitor intel notes, battlecard-ready summaries, and internal action notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs tag observations, inferences, overheard statements, estimates, and unknowns to separate evidence from interpretation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
