## Description:

Build a personal quotes system for saving, discovering, and automatically surfacing meaningful words.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users use this skill to capture meaningful quotes, organize them by author, topic, source, and favorites, and surface relevant quotes through manual lookup or configured delivery schedules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal quotes, conversation snippets, tags, and optional mood or context notes may contain private or emotionally sensitive information stored locally in ~/quotes/.

Mitigation: Use the skill only when local storage of this material is acceptable, and avoid saving sensitive quotes or context notes that should not persist.

Risk: Automatic delivery can surface private or sensitive quotes unexpectedly if schedules, categories, or notification channels are too broad.

Mitigation: Configure explicit delivery schedules, categories, and channels before enabling automatic quote surfacing.

Risk: Quotes can lose usefulness or become misleading if attribution and source context are missing or incorrect.

Mitigation: Verify authorship when possible and save source, tags, and context with each quote.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/quotes)
- [ClawHub publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown guidance and file organization patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local quote collection files under ~/quotes/ when the agent is asked to save or organize quotes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
