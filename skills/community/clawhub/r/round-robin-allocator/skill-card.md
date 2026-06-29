## Description: <br>
Allocates N objects across T rounds among K options according to proportions, maximizing coverage diversity and offering post-processing modes for repeat distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, planners, educators, and operations teams use this skill to turn natural-language allocation requests into proportional round-robin assignments and reports for projects, students, users, strategies, or similar recurring assignments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated HTML reports load Chart.js and Plotly from jsdelivr when opened. <br>
Mitigation: Use --no-html or --no-open for controlled or offline use, and review generated HTML before sharing. <br>
Risk: The skill creates local report files such as Markdown, CSV, and HTML outputs. <br>
Mitigation: Run it in an intended workspace and review output paths before retaining or distributing generated files. <br>
Risk: The --always option can skip future confirmation tables. <br>
Mitigation: Use --always only when future runs should intentionally bypass confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/round-robin-allocator) <br>
- [Usage guide](references/usage.md) <br>
- [Algorithm notes](references/algorithm.md) <br>
- [FAQ](references/faq.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown allocation reports, optional CSV exports, and HTML visualization files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated HTML visualizations load Chart.js and Plotly from jsdelivr when opened.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release, frontmatter, _meta.json, changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
