## Description:

Helps an agent collect required profile inputs, obtain consent, call Vestafolio's choisir-regime simulator API, and explain eligible French business legal forms with a qualitative recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vestafolio](https://clawhub.ai/user/vestafolio)

### License/Terms of Use:

MIT-0

## Use Case:

External users considering a French business structure use the skill to determine eligibility for micro-entreprise, EI, EURL, SASU, SARL, SAS, SELARL, and SELAS and receive a qualitative recommendation from Vestafolio's simulator.

### Deployment Geography for Use:

France

## Known Risks and Mitigations:

Risk: Using the simulator sends the user's activity type, projected turnover, existing-business status, liability preference, partner status, and unemployment-insurance preference to Vestafolio.

Mitigation: The skill requires explicit user agreement after summarizing the exact fields to be sent, omits names, addresses, credentials, files, and conversation history, and offers the manual simulator link if the user declines.

Risk: The result is qualitative business-structure guidance and may not reflect every legal or personal circumstance.

Mitigation: The skill grounds the answer in the API result, states assumptions and limits, and describes the output as orientation rather than legal advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vestafolio/skills/vestafolio-choisir-regime)
- [Vestafolio choisir-regime API](https://www.vestafolio.com/api/tools/v1/choisir-regime)
- [Vestafolio choisir-regime simulator](https://www.vestafolio.com/simulateurs/choisir-regime)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown response grounded in the simulator API result]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Replies in French when the user writes in French; asks for consent before sending required profile fields to Vestafolio.]

## Skill Version(s):

1.0.2 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
