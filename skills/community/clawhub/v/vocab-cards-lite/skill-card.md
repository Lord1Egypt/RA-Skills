## Description:

Generates printable black-and-white English vocabulary flashcard PNG images from JSON word lists, including main cards, optional side cards, and optional Baidu Baike QR-code cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[51comic](https://clawhub.ai/user/51comic)

### License/Terms of Use:

MIT-0

## Use Case:

External users, educators, and agents use this skill to convert English vocabulary JSON lists into printable vocabulary flashcard image sets with bilingual definitions, examples, optional side cards, and optional QR-code cards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation can affect the host Python environment.

Mitigation: Install in a virtual environment, avoid root execution, and use --allow-global only after accepting the system-level installation risk.

Risk: Pinned dependencies may still require local review before important deployments.

Mitigation: Review or update the pinned versions in requirements.txt before use on important systems.

Risk: User-provided baike_url values are encoded into generated QR images.

Mitigation: Verify QR target URLs before sharing or printing generated cards.

Risk: Generated cards may include Chinese text and depend on system CJK and DejaVu fonts.

Mitigation: Install trusted system fonts and review generated card content before distribution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/51comic/skills/vocab-cards-lite)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)
- [References - vocab-cards-lite](references/REFERENCES.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [PNG image files with console status messages and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a main card for each valid word entry, plus optional QR-code and side-card PNGs when the input provides baike_url or side data.]

## Skill Version(s):

2.0.4 (source: frontmatter, changelog, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
