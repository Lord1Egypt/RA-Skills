## Description:

Generates AI-readable DESIGN.md design-system guidance for Vibe coding applications, with bilingual site support, product-inspired templates, and a nine-part design specification structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI application builders use this skill to generate Markdown design-system specifications for Vibe coding workflows. Agents can then read the generated DESIGN.md guidance to produce UI code with more consistent visual themes, typography, layout, components, and responsive behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation and packaged files describe 58 templates, but the current CLI may not expose every packaged template as a selectable option.

Mitigation: Run `python3 scripts/generate.py --list` before relying on a specific template, and review or patch `scripts/generate.py` if a packaged template is needed but not selectable.

Risk: Generated design guidance may vary in completeness because the evidence notes documentation and feature-coverage mismatches across templates.

Mitigation: Review generated DESIGN.md files against the target product, brand, accessibility, and responsive-design requirements before using them to drive UI implementation.

Risk: The generator writes to a user-selected output path.

Mitigation: Choose output paths deliberately and review generated files before downstream agents use them to create or modify application code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/skills/vibe-coding-design-system)
- [README](README.md)
- [Introduction](INTRODUCTION.md)
- [Code audit report](CODE_AUDIT_REPORT.md)
- [Improvement plan](IMPROVEMENT_PLAN.md)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown DESIGN.md files with inline code snippets and optional JSON configuration inputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3 and writes generated design guidance to a user-selected output path.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
