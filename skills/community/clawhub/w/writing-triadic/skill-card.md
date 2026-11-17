## Description:

Writing Triadic is a three-role collaborative writing skill that mines intent, generates and evaluates drafts, supports style cloning, SEO workflows, instant drafting, and long-form chapter management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sallyface0](https://clawhub.ai/user/sallyface0)

### License/Terms of Use:

MIT-0

## Use Case:

Writers, marketers, students, and developers use this skill to turn writing goals into structured drafts, reader-style reviews, revisions, and reusable writing preferences across common formats such as blogs, essays, product copy, resumes, SEO content, and long-form documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive drafts, style profiles, or writing preferences may be processed by external model providers unless local privacy mode is configured.

Mitigation: Use local privacy mode for sensitive work, review the configured model providers before use, and avoid sharing sensitive drafts with non-local models.

Risk: The skill can create persistent writing profiles, session files, and knowledge-base records that may retain personal writing habits or confidential draft content.

Mitigation: Inspect or delete MEMORY.md, session folders, and the knowledge base when long-term profiling is not desired, and use the documented deletion commands where supported.

Risk: Server security evidence marks the release as suspicious because privacy promises may not match default external-model and storage behavior.

Mitigation: Review the skill carefully before installing, constrain the writing workspace, and confirm consent gates and local-model settings before processing private material.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sallyface0/skills/writing-triadic)
- [Publisher Profile](https://clawhub.ai/user/sallyface0)
- [README](README.md)
- [English README](README_EN.md)
- [Privacy and Data Governance](PRIVACY.md)
- [Changelog](CHANGELOG.md)
- [AI Trace Avoidance Guide](references/ai-traces-guide.md)
- [Template Library](references/template-library.md)
- [Style Cloning Guide](references/style-cloning-guide.md)
- [SEO Module](references/seo-module.md)
- [Instant Mode Protocol](references/instant-mode-protocol.md)
- [Long-Form Protocol](references/long-form-protocol.md)
- [State Contract](references/state-contract.md)
- [Model Configuration](references/model-config.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown drafts, review notes, writing plans, session state files, memory updates, and structured guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent writing profiles, session folders, knowledge-base notes, draft files, reader scorecards, SEO analyses, and style-clone fingerprints in the configured writing workspace.]

## Skill Version(s):

2.10.0 (source: server release metadata, SKILL.md frontmatter, CHANGELOG dated 2026-07-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
