## Description: <br>
Supports analysis, design, implementation, evaluation, dashboards, decision scenarios, and normative guidance for integrated hospitalization systems, with emphasis on hospital-at-home and hospital-to-home continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare operations, public-health, and hospital leadership teams use this skill to reason about integrated hospitalization, hospital-at-home operations, continuity risks, Chilean HD regulation, implementation planning, audits, dashboards, and decision scenarios. It supports system analysis and planning, not individual diagnosis, prescribing, or replacement of human clinical leadership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An embedded authenticated webhook token could allow unintended or unauthorized external calls. <br>
Mitigation: Remove the token from the skill package, rotate the credential, and require deployment-time secret injection instead of storing credentials in artifact files. <br>
Risk: Inter-agent delegation could send sensitive healthcare case context outside the skill boundary. <br>
Mitigation: Disable delegation by default or document exact destinations, data sent, consent requirements, and redaction rules before use. <br>
Risk: Declared runtime capabilities may not match the tool instructions included in the artifact. <br>
Mitigation: Align the manifest/runtime capability declaration with the documented tool behavior and review the resulting permission boundary before installation. <br>
Risk: The skill covers healthcare operations and regulation, where stale or unsupported guidance can affect safety and compliance. <br>
Mitigation: Treat bundled material as a baseline, externally verify current legal validity and recent policy changes, and keep human clinical and operational leadership accountable for decisions. <br>


## Reference(s): <br>
- [Salubrista HaH ClawHub release page](https://clawhub.ai/felix-antonio-sl/salubrista-hah) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Agent workflow and routing](artifact/references/agent/AGENTS.md) <br>
- [Agent tool map](artifact/references/agent/TOOLS.md) <br>
- [Chilean HD regulation baseline](artifact/references/knowledge/hodom/normativa/01-reglamento-hodom-ds1-2022.md) <br>
- [Chilean HD technical norm 2024](artifact/references/knowledge/hodom/normativa/03-norma-tecnica-hodom-2024.md) <br>
- [Hospital-at-home operating model](artifact/references/knowledge/hodom/director/02-manual-alta-complejidad.md) <br>
- [Chile hospital-at-home context 2024-2026](artifact/references/knowledge/hodom/director/03-situacion-chile-2026.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown analysis, recommendations, tables, reports, dashboards, maps, briefs, and decision scenarios] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include synthesis, scale, dominant modality, assumptions, local data gaps, continuity and safety risks, monitoring path, and normative or evidence trace when relevant.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
