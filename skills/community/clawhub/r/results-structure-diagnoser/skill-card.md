## Description:

Diagnoses macro-structure and organization of English psychology Results sections across eight dimensions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin77-chris](https://clawhub.ai/user/bin77-chris)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, editors, and academic writing assistants use this skill to review English psychology or cognitive neuroscience Results sections for macro-structure, including result ordering, hypothesis/RQ mapping, general-to-specific flow, figure/table introduction, result layering, multi-experiment organization, and Results-Discussion boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled instructions and default report template are largely Chinese, which may be unexpected for non-Chinese users.

Mitigation: Review language behavior during onboarding; the skill states feedback should follow the user's input language.

Risk: Structure diagnosis can be misleading when the user provides only partial Results text.

Mitigation: Mark missing global context as information insufficient and avoid absolute claims unless the complete Results input has been checked.

Risk: Rearrangement suggestions could be mistaken for language polishing or newly supplied research content.

Mitigation: Constrain outputs to structural rearrangement and referral notes; do not invent hypotheses, statistics, figures, results, or study design details.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bin77-chris/skills/results-structure-diagnoser)
- [Server-resolved GitHub provenance](https://github.com/bin77-chris/results-structure-diagnoser/tree/main/results-structure-diagnoser)
- [Boundary Guide](references/boundary_guide.md)
- [Checklist](references/checklist.md)
- [Hierarchy Rules](references/hierarchy_rules.md)
- [Multi-Experiment Guide](references/multi_experiment_guide.md)
- [Rubric](references/rubric.md)
- [Examples](references/examples.md)
- [Report Template](assets/report_template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown diagnostic report with scoring tables and prioritized structure recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows the user's input language and limits recommendations to structure, referral notes, and evidence-based issue localization.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
