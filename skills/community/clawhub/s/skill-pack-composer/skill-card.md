## Description: <br>
Combines multiple Skills into a bundle and checks for slug, dependency, resource, and positioning conflicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this agent to review Skill bundles before release, including slug, dependency, resource, and responsibility conflicts. It produces auditable drafts, checklists, and next-step guidance rather than publishing or changing external systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad directory inputs may include unrelated sensitive files in generated audit summaries. <br>
Mitigation: Run the skill only against the specific Skill or bundle directories intended for review and inspect generated reports before sharing. <br>
Risk: Generated bundle recommendations may be incomplete if the input directories or file lists are partial. <br>
Mitigation: Treat outputs as review drafts, confirm missing items, and verify dependency and resource conflicts before release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/52YuanChangXing/skill-pack-composer) <br>
- [README](README.md) <br>
- [Specification](resources/spec.json) <br>
- [Output Template](resources/template.md) <br>
- [Smoke Test](tests/smoke-test.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown reports, optional JSON output, and review-oriented shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local, review-oriented outputs; optional files are written only when the user supplies an output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
