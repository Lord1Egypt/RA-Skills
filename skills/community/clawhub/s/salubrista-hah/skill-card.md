## Description:

Use this skill when the user needs analysis, design, implementation, evaluation, dashboards, decision scenarios, or normative guidance for integrated hospitalization systems with emphasis on hospital-at-home and hospital-to-home continuity, especially bed capacity, discharge, re-admissions, transition risk, Director Tecnico HD, or Chilean HD regulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl)

### License/Terms of Use:

MIT-0

## Use Case:

External healthcare leaders, hospital operations teams, Hospitalizacion Domiciliaria directors, quality teams, and public health planners use this skill to analyze integrated hospitalization and hospital-to-home continuity problems, design operating models, evaluate risks, and produce dashboards, briefs, or decision scenarios. It supports human clinical and operational leadership; it does not replace individual diagnosis, prescribing, or local regulatory review.

### Deployment Geography for Use:

Chile for Hospitalizacion Domiciliaria regulatory guidance; adaptable globally for integrated hospitalization system analysis when local context is provided.

## Known Risks and Mitigations:

Risk: The packaged agent tooling exposes a bearer token and describes internal plaintext HTTP delegation that can share healthcare case context.

Mitigation: Remove or disable the delegation mechanism before installation, rotate the exposed token, and require explicit user authorization plus data minimization before any case context is shared.

Risk: Medical advisory guidance may be applied beyond the packaged corpus or local legal validity.

Mitigation: Use the bundled corpus as a baseline only, verify current regulatory status and local policy before relying on time-sensitive claims, and keep final decisions under accountable human clinical and operational leadership.

## Reference(s):

- [Salubrista HaH Skill Definition](SKILL.md)
- [Agent User Profile and Output Preferences](references/agent/USER.md)
- [Agent Tooling and Routing Notes](references/agent/TOOLS.md)
- [Hospital at Home Evidence Corpus](references/knowledge/hodom/corpus-hah-completo.md)
- [Direccion Tecnica en Hospitalizacion Domiciliaria](references/knowledge/hodom/director/01-manual-direccion-tecnica.md)
- [Manual de Hospitalizacion Domiciliaria de Alta Complejidad](references/knowledge/hodom/director/02-manual-alta-complejidad.md)
- [Situacion de la Hospitalizacion Domiciliaria en Chile 2024-2026](references/knowledge/hodom/director/03-situacion-chile-2026.md)
- [Reglamento de Establecimientos que Otorgan Prestaciones de Hospitalizacion Domiciliaria](references/knowledge/hodom/normativa/01-reglamento-hodom-ds1-2022.md)
- [Decreto Exento 31/2024](references/knowledge/hodom/normativa/02-decreto-exento-31-2024-aprueba-norma-tecnica.md)
- [Norma Tecnica para Establecimientos de Hospitalizacion Domiciliaria](references/knowledge/hodom/normativa/03-norma-tecnica-hodom-2024.md)
- [LeyChile - Norma 1181901](https://www.leychile.cl/Navegar?idNorma=1181901)
- [MINSAL](https://www.minsal.cl)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured Markdown with optional KPI tables, risk maps, policy briefs, dashboards, and decision scenarios]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish technical-professional style; synthesis first; explicit scale, modality, assumptions, data gaps, continuity risks, safety risks, and normative or evidence trace when relevant.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
