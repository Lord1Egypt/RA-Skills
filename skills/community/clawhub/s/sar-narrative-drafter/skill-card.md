## Description:

Helps BSA officers, AML investigators, and FIU staff draft confidential FinCEN SAR Part V narratives with 5 W's + H coverage, FinCEN keyword tagging, FFIEC quality checks, and a BSA-officer review block.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

BSA officers, AML investigators, transaction-monitoring analysts, and FIU staff use this skill to turn suspicious-activity case files into draft FinCEN SAR Part V narrative packets for institutional review before any filing decision or submission.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Confidential SAR material or sensitive identifiers could be exposed if users paste full SSNs, EINs, account numbers, or card numbers into the chat.

Mitigation: Use the skill only in authorized BSA/AML compliance workflows and provide last-4 identifiers in narrative drafting unless institutional policy requires otherwise.

Risk: Draft narratives, FinCEN keyword tags, or filing posture could be incorrect without institutional review.

Mitigation: Verify current FinCEN keywords, facts, deadlines, and filing decisions through the institution's approved BSA officer review process before any submission.

Risk: A user could misunderstand the draft as a SAR filing or as contact with FinCEN or law enforcement.

Mitigation: Treat every output as a draft only; the skill does not submit SARs, access FinCEN BSA E-Filing, contact law enforcement, or decide whether the filing threshold is met.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/sar-narrative-drafter)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown draft narrative packet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft output includes FinCEN keyword tags, a 5 W's + H coverage matrix, FFIEC quality self-check, weak-language audit, retention note, unresolved-information list, and BSA-officer review block.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
