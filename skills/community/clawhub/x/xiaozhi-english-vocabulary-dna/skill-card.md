## Description:

按学生表现安排英语词汇的间隔复习，并生成每日词卡和课前预热练习。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qizhitang](https://clawhub.ai/user/qizhitang)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking students use this skill to save English vocabulary, review it on a personalized spaced-repetition schedule, and preview words before lessons. It also supports vocabulary progress summaries and, with consent, learning-profile updates and reminder handoffs.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The security scan was partial, reported a low-probability Unicode warning, and could not match three references in SKILL.md to bundled components.

Mitigation: Review the unmatched references and Unicode-bearing text before installation; the scan guidance notes that a benign verdict does not mean risk-free.

Risk: Vocabulary history and learning progress may be stored or shared through profile updates and reminder handoffs.

Mitigation: Follow the skill's consent checks and user controls before saving profile data, sharing across skills, or enqueueing reminders.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/qizhitang/skills/xiaozhi-english-vocabulary-dna)
- [English high-school vocabulary reference](artifact/references/english-hs-vocabulary.md)
- [Vocabulary radar topics](artifact/references/vocabulary-radar-topics.md)
- [Spaced-repetition schedule guidance](artifact/shared/ebbinghaus-schedule.md)
- [Crisis exception guidance](artifact/shared/crisis-exception.md)

## Skill Output:

**Output Type(s):** [Text, Guidance, Structured data]

**Output Format:** [Chinese conversational text and structured vocabulary, profile, and reminder handoffs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily due words are consolidated into one card; profile updates and reminder handoffs require the relevant consent.]

## Skill Version(s):

2.12.7 (source: evidence release and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
