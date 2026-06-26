## Description: <br>
Taxonomy Normalizer helps users reconcile category systems across teams or tables while preserving alias mappings and deprecated terms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Data stewards, analysts, and developers use this skill to turn category lists, aliases, and conflict notes into an auditable taxonomy-normalization draft with migration suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated taxonomy mappings or migration suggestions may be incomplete or incorrect if the supplied category data is ambiguous. <br>
Mitigation: Treat outputs as review drafts and confirm unresolved conflicts, aliases, and deprecated terms before acting on them. <br>
Risk: Local file input and output paths could expose or overwrite unintended materials if selected carelessly. <br>
Mitigation: Review input and output paths before running the script, and avoid pointing it at sensitive directories or files unnecessarily. <br>
Risk: Taxonomy normalization can accidentally erase meaningful business differences between teams or datasets. <br>
Mitigation: Use the skill's conflict and overlap sections to preserve distinctions for reviewer approval instead of forcing automatic unification. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/52YuanChangXing/taxonomy-normalizer) <br>
- [Publisher profile](https://clawhub.ai/user/52YuanChangXing) <br>
- [README](artifact/README.md) <br>
- [Structured specification](artifact/resources/spec.json) <br>
- [Output template](artifact/resources/template.md) <br>
- [Example output](artifact/examples/example-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Structured Markdown report by default, with optional JSON output from the local script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 for script execution; reads local input files or directories and writes to stdout or a selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
