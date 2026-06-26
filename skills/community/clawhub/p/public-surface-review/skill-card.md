## Description: <br>
Publish Guard audits README, SKILL.md, launch docs, agent metadata, and leak patterns before GitHub or ClawHub publication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and maintainers use Publish Guard before publishing a GitHub repository or ClawHub skill to identify secret-shaped strings, internal launch artifacts, weak first-run copy, and public-audience issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports can expose sensitive filenames and line numbers for possible secret findings, even when snippets are redacted. <br>
Mitigation: Run the skill against a specific repository rather than a broad filesystem path, and treat generated reports as sensitive until reviewed. <br>
Risk: Heuristic scans for leak patterns, public-audience mismatch, and launch-copy readiness can miss issues or flag benign content. <br>
Mitigation: Use the report as a pre-release review aid and manually confirm findings before publishing or sharing the results. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/public-surface-review) <br>
- [Project homepage](https://zack-dev-cm.github.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown audit with supporting JSON scan outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include a publish recommendation, launch-copy score, and summarized leak and public-surface findings.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
