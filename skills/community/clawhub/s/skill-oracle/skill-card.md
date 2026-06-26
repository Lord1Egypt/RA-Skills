## Description: <br>
Skill Oracle is curated documentation of quality ClawHub skills, using Markdown tables and static JSON to tell agents which tools work and which are empty. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[certainlogicai](https://clawhub.ai/user/certainlogicai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to discover and compare ClawHub skills, select recommended tools for productivity, security, business, development, and self-improvement workflows, and see limitations before installing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional helper can load local external Company Brain code and inject local knowledge-base content into prompts. <br>
Mitigation: Review or disable brain_enhance.py before installing when only the static catalog is desired. <br>
Risk: The catalog includes install commands and paid-product suggestions that an agent may surface during recommendations. <br>
Mitigation: Require manual approval before running recommended clawhub install commands or acting on paid-product suggestions. <br>
Risk: The catalog is curated and static, so recommendations may be incomplete, stale, or biased toward skills the publisher tested. <br>
Mitigation: Check the referenced skill pages and current ClawHub metadata before relying on a recommendation for production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/certainlogicai/skill-oracle) <br>
- [Skill Oracle Documentation](https://certainlogic.ai/docs/skill-oracle) <br>
- [Company Brain Core OS](https://certainlogic.ai/brain) <br>
- [Self-Improving Agent Tools Scan](docs/self-improving-scan-2026-05-09.md) <br>
- [Catalog Schema Guide](docs/SCHEMA.md) <br>
- [W3C PROV Overview](https://www.w3.org/TR/prov-overview/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables, static JSON metadata, and inline shell install commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static catalog content; optional helper can enrich prompts from a local Company Brain installation when present.] <br>

## Skill Version(s): <br>
1.0.6 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
