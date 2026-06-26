## Description: <br>
Skill Vetter Optimized helps agents review third-party skills before installation by checking source reputation, permissions, suspicious patterns, and overall risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[confidentkai](https://clawhub.ai/user/confidentkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill before installing unknown or third-party skills to perform structured source, code, permission, and risk reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A review aid can miss risky behavior or produce misleading comfort if its output is treated as a complete security guarantee. <br>
Mitigation: Use it as an initial review aid, manually inspect flagged patterns, and complete a human security review before installing unknown skills. <br>
Risk: Running the checker across broad private folders can expose more local filenames and metadata than intended. <br>
Mitigation: Run the checker only against the specific skill directory intended for inspection. <br>


## Reference(s): <br>
- [Systematic skill review checklist](references/checklist.md) <br>
- [ClawHub skill listing](https://clawhub.ai/confidentkai/skill-vetter-optimized) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown review report with optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script emits a local text summary of skill metadata, file counts, script files, and detected risk patterns.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter, changelog, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
