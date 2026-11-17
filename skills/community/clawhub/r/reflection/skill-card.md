## Description:

Helps agents pause for self-review, learn from corrections, detect recurring patterns, and surface prior lessons before delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and developers use Self Reflection to add pre-delivery review, post-correction logging, recurring pattern detection, and proactive lesson surfacing to agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist corrections, patterns, and user-specific lessons in local reflection files without explicit retention or redaction rules.

Mitigation: Review ~/reflection/ periodically, avoid storing secrets or sensitive project details, and add local rules for consent, redaction, retention, and deletion before broad use.

Risk: Incorrectly logged lessons or detected patterns could bias future agent responses.

Mitigation: Review proposed reflections and prevention rules before treating them as reusable guidance, especially after user corrections or high-impact work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/reflection)
- [Skill homepage](https://clawic.com/skills/reflection)
- [Setup guide](artifact/setup.md)
- [Memory template](artifact/memory-template.md)
- [Evaluation dimensions](artifact/dimensions.md)
- [Reflection prompts](artifact/prompts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and local file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates persistent local reflection files under ~/reflection/ when followed.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
