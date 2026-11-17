## Description:

Plan participant recruitment for a UserTold Study and produce participant-readable recruitment copy plus canonical Invitation, Visibility, and neutral Intake inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usertold](https://clawhub.ai/user/usertold)

### License/Terms of Use:

MIT-0

## Use Case:

External research, product, and customer teams use this skill to plan truthful participant recruitment for UserTold studies. It helps define reachable participant boundaries, choose outreach channels, draft participant-facing copy, set reward terms, and produce canonical Invitation, Visibility, and Intake inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated recruitment invitations, rewards, eligibility rules, or intake questions may be inaccurate or misaligned with privacy, legal, or organizational policy requirements.

Mitigation: Review all generated participant copy and canonical JSON before use, and obtain explicit approval before activating or updating any live UserTold Study settings.

Risk: Recruitment plans can overstate coverage or imply representative sampling when based on reachable convenience audiences.

Mitigation: Keep the skill's sampling-bias note in research readouts and avoid representative-sample claims unless separately supported.

## Reference(s):

- [UserTold skill page](https://clawhub.ai/usertold/skills/usertold-recruit-participants)
- [Channel selection](references/channel-selection.md)
- [Invitation examples](references/invitation-examples.md)
- [Rewards](references/rewards.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with canonical JSON objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces recruitment plans, participant-facing copy, and UserTold Invitation, Visibility, intake_create, and intake_update inputs; requires explicit approval before live changes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
