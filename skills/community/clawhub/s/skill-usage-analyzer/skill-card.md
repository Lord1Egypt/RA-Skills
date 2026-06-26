## Description: <br>
Analyzes OpenClaw SKILL.md files and generates human-friendly usage guides with examples, configuration details, warnings, best practices, recommendations, comparisons, and skill-combination ideas. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoxiao19810912](https://clawhub.ai/user/xiaoxiao19810912) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inspect installed or local skills and quickly understand how to run them, what they produce, and how they can be combined or compared. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads SKILL.md files and lists filenames in analyzed skill directories, which can expose private project or skill names if pointed at unrelated directories. <br>
Mitigation: Run it only against intended OpenClaw skill directories and avoid private directories where filename disclosure would matter. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoxiao19810912/skill-usage-analyzer) <br>
- [README](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON reports with optional command examples and generated recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may be printed to stdout or written to a user-selected file.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, package.json, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
