## Description:

AI 中英互译与译文润色工作流。覆盖译前准备、分块翻译、两遍校对、术语一致性校验和文化适配，适用于论文、商务信函、技术文档和营销文案的翻译与精修。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users, translators, editors, and developers use this skill to translate and polish Chinese-English content with structured preparation, terminology controls, segmented translation, proofreading, and cultural adaptation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The glossary checker reads local translation files when validating terminology.

Mitigation: Run it only on files you are comfortable processing locally and review the command arguments before execution.

Risk: The learner script stores cross-session notes and preferences in learned_patterns.json.

Mitigation: Do not store client, legal, medical, personal, or confidential content in learner notes, and delete learned_patterns.json when retained history is no longer wanted.

Risk: The learner script can be pointed at local skill directories outside its default location.

Mitigation: Run learner.py only against this skill's own directory unless you have reviewed and approved the target directory.

Risk: AI-assisted translations for legal, medical, confidential, or high-impact documents may be incomplete or inaccurate.

Mitigation: Use human review for sensitive or critical translations and avoid processing classified or personal data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/translate-polish)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON glossary examples, and script-generated JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local translation files for terminology checks and may store learning history in learned_patterns.json when the learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
