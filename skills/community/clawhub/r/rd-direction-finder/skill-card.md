## Description:

Given an engineering or technical problem description, this skill decomposes R&D needs into demand drivers, bottlenecks, and solution paths, searches patents, papers, and web sources, and produces structured R&D direction recommendations with Markdown, HTML, and payload JSON reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

R&D teams, technical strategists, and patent researchers use this skill to turn a project problem statement into multiple evidence-backed research directions. It is intended for generating structured research reports that combine problem decomposition, patent and paper search, web evidence, and rendered report files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential R&D problem descriptions may be sent to external search or MCP services.

Mitigation: Use only approved search/MCP services and avoid submitting confidential text unless sharing is authorized.

Risk: Generated HTML reports may preserve active markup from user input or search-result content.

Mitigation: Do not open HTML generated from untrusted payloads or search content until the renderer escapes or sanitizes HTML and applies a restrictive content security policy.

Risk: The workflow writes Markdown, JSON, and HTML reports to disk.

Mitigation: Use approved workspace paths and review generated files before sharing them outside the intended project context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanzhian-patsnap/skills/rd-direction-finder)
- [Output paths](artifact/assets/paths.md)
- [Payload JSON schema](artifact/assets/payload-schema.md)
- [Report template](artifact/assets/report-template.md)
- [Workflow reference](artifact/assets/workflow.md)
- [PatSnap open platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, json, html, shell commands, configuration, guidance]

**Output Format:** [Markdown report, payload JSON, rendered HTML report, and concise command/configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces no more than max_directions R&D directions; default max_directions is 10.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog, created 2026-08-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
