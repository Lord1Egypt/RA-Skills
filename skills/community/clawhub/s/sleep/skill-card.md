## Description:

Coaches sleep with quantified protocols: insomnia CBT-I, jet lag light timing, shift work anchors, caffeine and melatonin cutoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for practical sleep coaching across insomnia, circadian timing, jet lag, shift work, sleep environment, substances, trackers, parasomnias, and life-stage modifiers. The skill triages red flags before protocol advice and routes medical warning signs to clinicians.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive sleep, health-adjacent, substance, household, prescription-context, and travel-plan details under ~/Clawic/data/sleep/.

Mitigation: Review that storage behavior before installation, avoid recording unnecessary sensitive details, and protect or delete the local directory when the data is no longer needed.

Risk: Sleep guidance can be inappropriate when symptoms indicate a medical condition such as apnea, severe sleepiness, narcolepsy, pregnancy-related breathing concerns, or depression-related insomnia.

Mitigation: Use the skill's red-flag triage before protocol advice and route warning signs to a clinician rather than continuing self-coaching.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/sleep)
- [Clawic Skill Page](https://clawic.com/skills/sleep)
- [Sleep Skill Definition](artifact/SKILL.md)
- [Setup](artifact/setup.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance, protocol tables, and local memory/configuration file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose user-maintained local files under ~/Clawic/data/sleep/ for diary, memory, trip plans, and preferences.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
