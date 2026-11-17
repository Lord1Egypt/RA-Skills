## Description:

Generates TOEFL iBT speaking practice sets with four progressively structured interview questions, reference answers, and answer explanations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saikewei](https://clawhub.ai/user/saikewei)

### License/Terms of Use:

MIT-0

## Use Case:

Students and TOEFL practice coaches use this skill to generate fresh speaking interview practice sets, reveal reference answers on request, and evaluate user responses against fluency, vocabulary, grammar, and content criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may retain generated answers and practice history in local files under toefl/.

Mitigation: Review or clear the local toefl/ files before sharing a workspace or publishing generated practice records.

Risk: Generating or changing a question set may update local Markdown and JSON files.

Mitigation: Run the skill in a workspace where updates to toefl/latest.md, toefl/history.json, and dated archives are expected.

## Reference(s):

- [Prompt Template](artifact/prompt-template.md)
- [ClawHub Skill Page](https://clawhub.ai/saikewei/skills/toefl-speaking)
- [Publisher Profile](https://clawhub.ai/user/saikewei)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown question sets with separated reference answers and answer explanations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The normal workflow may update local Markdown and JSON practice-history files under toefl/.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 2.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
