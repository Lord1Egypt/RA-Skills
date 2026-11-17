## Description:

Ziwei Fortune generates Zi Wei Dou Shu birth charts and interpretive Markdown reports from a user's lunar birth date, birth time, and gender.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eamanc-lab](https://clawhub.ai/user/eamanc-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill for entertainment and self-exploration through Zi Wei Dou Shu chart calculation, single-palace queries, major-limit readings, and constructive interpretations. It is not intended to replace medical, legal, financial, or other professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store and reuse personal birth-profile data, including lunar birth date, birth time, gender, and derived chart information, in local memory.

Mitigation: Ask the agent not to persist the data, confirm any reused profile values before analysis, and request review or deletion of MEMORY.md after use.

Risk: Fortune-telling output may be mistaken for professional or deterministic advice.

Mitigation: Use the report for entertainment or self-exploration only and rely on qualified professionals for medical, legal, financial, or other major decisions.

## Reference(s):

- [Calculation Rules](artifact/references/calculation-rules.md)
- [Interpretation Guide](artifact/references/interpretation-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/eamanc-lab/skills/ziwei-fortune)
- [Project Homepage](https://github.com/eamanc-lab/fortune-telling-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown report with tables, calculation trace, and narrative interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist lunar birth date, birth time, gender, and derived chart cache in a local MEMORY.md file.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
