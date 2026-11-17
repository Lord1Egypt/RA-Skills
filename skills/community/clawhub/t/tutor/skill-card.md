## Description:

Personalized tutoring for any age and subject with adaptive teaching, progress tracking, and parent oversight.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Learners, parents, and educators use this skill to run age-appropriate tutoring sessions across school, university, adult-learning, test-prep, language, writing, science, math, reading, and technical subjects. It guides an agent to teach through questions, adapt pacing, track progress, generate reports, and escalate safety concerns when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist sensitive learner and minor education records in predictable local plaintext files under ~/tutor/.

Mitigation: Use explicit consent, sanitized learner identifiers, owner-only file permissions, retention and deletion rules, and limits on sensitive notes before real learner use.

## Reference(s):

- [ClawHub Tutor Skill Page](https://clawhub.ai/ivangdavila/skills/tutor)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Conversational text and Markdown, with JSON and JSONL learner records when progress is saved]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores learner profiles, session logs, progress records, subject notes, and reports under ~/tutor/ when used as written.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
