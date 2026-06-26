## Description: <br>
Review Miner extracts selling points, pain points, objections, and phrases to avoid from reviews, ratings, and feedback for voice-of-customer and marketing analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, growth, customer support, and voice-of-customer teams use this skill to turn review text, CSV or TSV exports, and support summaries into reviewable findings and next-step checklists. It is suited to selling-point extraction, competitive research, customer feedback organization, and identifying claims that should not be reused. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review and support inputs may contain personal, sensitive, or customer-identifying information. <br>
Mitigation: Redact sensitive data before analysis and keep outputs limited to reviewable summaries and checklists. <br>
Risk: The local Python helper reads input paths and can write an output file when requested. <br>
Mitigation: Install only from a trusted publisher, prefer stdout or --dry-run when a file is unnecessary, and review output paths before execution. <br>
Risk: The bundled script contains unused audit modes that can scan local files if the spec is modified. <br>
Mitigation: Do not edit the bundled spec to enable unrelated audit modes unless that local scanning behavior is intentional. <br>
Risk: The skill could be misused to fabricate endorsements or expose user identities. <br>
Mitigation: Use it only to summarize provided evidence, avoid generating fake reviews, and remove identifying details from published material. <br>


## Reference(s): <br>
- [Review Miner on ClawHub](https://clawhub.ai/52YuanChangXing/review-miner) <br>
- [Artifact README](artifact/README.md) <br>
- [Review Miner Specification](artifact/resources/spec.json) <br>
- [Output Template](artifact/resources/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report by default, with an optional JSON wrapper around the report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 only; can print to stdout, write to an output file, run with --dry-run, and limit sampled rows or findings with --limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, target metadata, and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
