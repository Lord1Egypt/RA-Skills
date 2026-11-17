## Description:

Use this skill when the user wants to distill a real researcher, professor, advisor, lab, or research community into an evidence-grounded cyber mentor skill from papers, academic homepages, talks, interviews, CVs, Google Scholar/Semantic Scholar/OpenAlex/arXiv records, PDFs, Zotero libraries, or provided source folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwqalice](https://clawhub.ai/user/qwqalice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use this skill to build, update, validate, or critique evidence-grounded research mentor skill packages from public academic sources. It supports evidence collection, publication metadata gathering, full-text signal extraction, mentor profile synthesis, package validation, and optional export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts fetch arbitrary URLs from scholar pages and publication indexes.

Mitigation: Use the scripts only on trusted public scholar pages and trusted publication indexes, inspect collection reports, and avoid --allow-insecure-ssl unless a reviewer accepts the risk.

Risk: Publication collection can use environment API keys and persist reports or local content.

Mitigation: Keep reports private when API keys or sensitive paths may be exposed, and review generated files before sharing or committing them.

Risk: Exported packages may include symlinks or sensitive local files.

Mitigation: Run the MentorForge validator and inspect package contents before export or installation.

Risk: Generated mentor skills can overstate what public evidence supports.

Mitigation: Require direct evidence, strong inference, and speculative extension labels, and validate version claims against the documented v0-v3 gates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qwqalice/skills/research-mentor-distiller)
- [Publisher profile](https://clawhub.ai/user/qwqalice)
- [Server-resolved GitHub provenance](https://github.com/qwqalice/MentorForge/tree/main/research-mentor-distiller)
- [Compliance and Packaging](references/compliance-and-packaging.md)
- [Full-Text Distillation Protocol](references/fulltext-distillation-protocol.md)
- [Mentor Skill Template](references/mentor-skill-template.md)
- [Research Mentor Distillation Schema](references/profile-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with generated files, JSON manifests, YAML agent metadata, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated mentor skill packages are intended to include SKILL.md, agents/openai.yaml, distillation-manifest.json, evidence references, publication indexes, research taste profiles, full-text distillation notes, and validation reports.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
