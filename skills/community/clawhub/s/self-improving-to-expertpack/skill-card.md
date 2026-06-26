## Description: <br>
Converts Self-Improving Agent learning files and promoted workspace guidance into an Obsidian-compatible ExpertPack with a manifest, overview, categorized content, and relationship files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianhearn](https://clawhub.ai/user/brianhearn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to migrate local Self-Improving Agent learnings into a portable ExpertPack for backup, review, publishing, or use in another agent environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The export can package private workspace instructions, customer data, or stale local agent rules into a shareable ExpertPack. <br>
Mitigation: Before publishing, committing, or sharing the generated ExpertPack, manually inspect the output for private instructions, customer data, and unsafe or outdated rules. <br>
Risk: Automatic secret stripping is pattern-based and may miss sensitive values while overstating the safety of the generated output. <br>
Mitigation: Treat automatic redaction as incomplete; scan and review generated files for secrets and credentials before relying on or sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianhearn/self-improving-to-expertpack) <br>
- [ExpertPack homepage](https://expertpack.ai) <br>
- [ExpertPack ClawHub skill](https://clawhub.com/skills/expertpack) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown files, YAML configuration, and command-line status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes an ExpertPack directory containing manifest.yaml, overview.md, categorized content files, optional glossary.md, and relations.yaml.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
