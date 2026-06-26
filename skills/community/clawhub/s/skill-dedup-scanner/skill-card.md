## Description: <br>
Scans installed skills for duplicates, naming conflicts, and similar descriptions that may cause model confusion, with English and Chinese output support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shyjsarah](https://clawhub.ai/user/shyjsarah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit installed skill collections before publishing new skills or troubleshooting trigger conflicts. It reports similar skill pairs, similarity scores, conflict severity, and recommendations for clarifying or renaming skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad skill-auditing requests may route to this skill when the user did not intend to run a duplicate scan. <br>
Mitigation: Invoke it with explicit duplicate-scan or conflict-scan wording, and review the generated report before acting on recommendations. <br>
Risk: Reports can be incomplete or misleading when scanned skills have missing or malformed SKILL.md frontmatter. <br>
Mitigation: Check flagged skill files directly before merging, renaming, or removing skills based on the report. <br>


## Reference(s): <br>
- [Skill Naming Best Practices](references/best_practices.md) <br>
- [ClawHub release page](https://clawhub.ai/shyjsarah/skill-dedup-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Markdown report or JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scan directory, skill count, similarity scores, conflict severity, recommendations, and optional file output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
