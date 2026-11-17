## Description:

Provides direct, practical coaching for adult romantic and sexual relationships, including conflict, attachment, trust, intimacy, desire, flirting, consent, and repair, with safety redirects for danger, coercion, minors, non-consent, self-harm, stalking, and professional-scope issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tristanmanchester](https://clawhub.ai/user/tristanmanchester)

### License/Terms of Use:

MIT-0

## Use Case:

External adult users use this skill for concrete relationship-coaching responses, scripts, worksheets, and structured next steps around romantic conflict, attachment patterns, dating, intimacy, desire, kink-aware consent, repair, and stay-or-leave reflection. It is not a substitute for therapy, legal advice, medical care, safeguarding, or crisis support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may discuss adult sexual topics, desire, kink, and intimate conflict.

Mitigation: Deploy it only where adult relationship-coaching content is appropriate, and keep the documented safety triage for coercion, minors, non-consent, crisis, stalking, and abuse cases.

Risk: The bundled validation and smoke-test scripts can execute Python from a user-selected target folder.

Mitigation: Run optional scripts only against trusted or isolated folders, preferably in a disposable environment without sensitive writable paths.

Risk: Relationship guidance can be misused to pressure, surveil, manipulate, or diagnose a partner.

Mitigation: Use the safety and edge-case references to redirect manipulation, surveillance, coercion, violence, non-consent, and diagnosis requests toward boundaries, safety support, or professional help.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tristanmanchester/skills/relationship-science-coach)
- [Source map and evidence basis](artifact/references/SOURCE_MAP.md)
- [Operating model](artifact/references/OPERATING_MODEL.md)
- [Intervention library](artifact/references/INTERVENTION_LIBRARY.md)
- [Safety semantic triage](artifact/references/SAFETY_SEMANTIC_TRIAGE.md)
- [Conflict, attachment, repair, and trust](artifact/references/CONFLICT_ATTACHMENT_AND_REPAIR.md)
- [Sex, intimacy, and desire](artifact/references/SEX_INTIMACY_AND_DESIRE.md)
- [Dating, flirting, and attraction](artifact/references/DATING_FLIRTING_AND_ATTRACTION.md)
- [Worksheet templates](artifact/assets/worksheet-templates.md)
- [Gottman Method overview](https://www.gottman.com/about/the-gottman-method/)
- [EFCT systematic review and meta-analysis](https://pubmed.ncbi.nlm.nih.gov/30605013/)
- [Dual Control Model](https://kinseyinstitute.org/research/dual-control-model.html)
- [Sexual strangulation risks](https://bwell.brown.edu/tool/sexual-strangulation)
- [988 Lifeline](https://988lifeline.org/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON coaching plans, scripts, worksheets, and concise guidance, with optional shell commands for local helper scripts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional scripts write structured data to stdout and diagnostics to stderr; the skill is designed to avoid network access.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
