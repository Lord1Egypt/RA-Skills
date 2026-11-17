## Description:

Safety planning resources and procedures for leaving dangerous living situations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users and support agents use this skill to respond to disclosures of domestic violence, abuse, unsafe housing, or urgent exit planning needs with crisis contacts, digital-safety guidance, safety planning checklists, and legal-resource pointers.

### Deployment Geography for Use:

Global, with US-specific hotline and legal-resource defaults that require localization for non-US users.

## Known Risks and Mitigations:

Risk: The release requests broad filesystem access even though the evidence does not show a clearly scoped file feature.

Mitigation: Install only in an environment where local filesystem access is acceptable, or require a safer release that removes filesystem access unless a user-approved file feature is added.

Risk: The install command uses an unpinned npx path.

Mitigation: Pin or verify the reviewed release before installation and avoid relying on an unversioned installer path for sensitive deployments.

Risk: The skill handles safety-critical domestic violence and exit-planning scenarios with US-specific defaults.

Mitigation: Lead with immediate danger assessment and crisis contacts, localize non-US resources before advising, and defer personalized planning to trained domestic violence professionals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/howtousehumans/skills/safe-exit-planner)
- [National Domestic Violence Hotline](https://www.thehotline.org/)
- [NNEDV Safety Planning with Technology](https://www.techsafety.org/resources-survivors/technology-safety-plan)
- [WomensLaw State Law Information](https://www.womenslaw.org/laws)
- [Legal Services Corporation LawHelp](https://www.lawhelp.org/)
- [Signal Foundation](https://signal.org/)
- [Danger Assessment](https://www.dangerassessment.org/)
- [Find a Helpline](https://findahelpline.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with crisis contacts, safety checklists, secure communication steps, and legal-resource pointers.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes US-specific hotline and legal-resource defaults; localize for non-US users and avoid storing sensitive safety details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
