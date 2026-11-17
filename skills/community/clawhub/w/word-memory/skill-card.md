## Description:

Word Memory helps learners practice English vocabulary with Ebbinghaus-style review scheduling, quizzes, lookup, and local progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg)

### License/Terms of Use:

MIT-0

## Use Case:

External users and language learners use this skill to plan daily vocabulary study, review due words, take short quizzes, query word details, and track progress locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores study progress and preferences locally.

Mitigation: Use it only in a workspace where local progress files are acceptable, and avoid entering sensitive personal information into vocabulary notes or settings.

Risk: Documentation mentions network dictionary lookup and daily reminder features that are not implemented in the inspected code.

Mitigation: Review future releases and permissions before enabling versions that add network access, scheduled reminders, or external dictionary integrations.

Risk: Vocabulary definitions, examples, and word lists are limited and may not be authoritative.

Mitigation: Verify learning content before relying on it for exams, instruction, or other high-stakes language study.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cp3d1455926-svg/skills/word-memory)
- [Publisher profile](https://clawhub.ai/user/cp3d1455926-svg)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown-style text responses with vocabulary plans, quiz prompts, word details, progress summaries, and setting confirmations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are primarily Chinese-language learner guidance and may create or update local progress JSON files when the Python helper is used.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
