## Description:

Helps an agent analyze uploaded tongue photos using Traditional Chinese Medicine tongue-observation references and produce a structured, disclaimer-bearing wellness assessment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwbwin](https://clawhub.ai/user/wwbwin)

### License/Terms of Use:

MIT-0

## Use Case:

External users can upload tongue photos or request tongue-observation analysis to receive a structured TCM-style report covering visible tongue features, a wellness rating, possible areas of concern, daily-care guidance, and medical disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is framed around medical diagnosis and broad health triggers, so users may over-rely on its tongue-photo assessment.

Mitigation: Present outputs as reference-only wellness information, do not rule illness in or out, and direct users with symptoms or concerns to a qualified clinician.

Risk: Uploaded mouth photos can expose sensitive personal health information.

Mitigation: Use the skill only where uploaded images can be handled privately and avoid retaining or sharing photos beyond the user's intended session.

Risk: The artifact includes daily-care and TCM-style guidance that could be mistaken for treatment advice.

Mitigation: Keep guidance conservative, avoid medication or prescription recommendations, and include the required medical disclaimer in each report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wwbwin/skills/tongue-diagnosis)
- [report-template.md](references/report-template.md)
- [sublingual-supplement.md](references/sublingual-supplement.md)
- [syndrome-patterns.md](references/syndrome-patterns.md)
- [tongue-body.md](references/tongue-body.md)
- [tongue-coating.md](references/tongue-coating.md)
- [tongue-lines-supplement.md](references/tongue-lines-supplement.md)
- [tongue-sublingual.md](references/tongue-sublingual.md)
- [tongue-zones.md](references/tongue-zones.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes tongue-feature observations, wellness rating, possible concerns, daily-care suggestions, and a medical disclaimer.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
