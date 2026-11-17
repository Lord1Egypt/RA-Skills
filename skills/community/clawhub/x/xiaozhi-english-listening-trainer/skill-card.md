## Description:

Personalizes English listening practice to a learner’s vocabulary and interests, then helps identify whether comprehension difficulties come from vocabulary, sentence structure, or listening speed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

Upper-primary, middle-school, and high-school English learners use the skill to practice with level-matched passages, comprehension questions, vocabulary notes, and targeted follow-up. Upper-primary learners are expected to use it with a parent or teacher present.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is benign with no listed findings, but the analysis was partial because two SKILL.md references did not match bundled artifacts.

Mitigation: Review the referenced source materials before relying on the skill; treat the benign scan as incomplete evidence.

Risk: Without speech synthesis or a reader, the fallback is a reading-based exercise rather than actual listening practice.

Mitigation: Clearly label the fallback as a transition activity and explain that it is not listening training.

Risk: The skill supports upper-primary learners and may encounter disclosures outside ordinary learning support.

Mitigation: Use with a parent or teacher present; when crisis signals arise, stop the learning flow and follow the documented referral guidance.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-english-listening-trainer)
- [Listening topic templates](artifact/references/listening-topic-templates.md)
- [Question quality checklist](artifact/shared/ai-item-check.md)
- [Crisis referral guidance](artifact/shared/crisis-referral-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Conversational text with English listening passages, comprehension questions, vocabulary notes, and learner feedback]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Passage difficulty and topics are personalized; without audio support, the skill labels read-aloud or timed-reading alternatives as a transition rather than listening practice.]

## Skill Version(s):

2.12.7 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
