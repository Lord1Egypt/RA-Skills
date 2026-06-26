## Description: <br>
Security vetting protocol before installing any AI agent skill, with red flag detection for credential theft, obfuscated code, exfiltration, and LOW/MEDIUM/HIGH/EXTREME risk classification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[firebroo](https://clawhub.ai/user/firebroo) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill before installing or running AI agent skills from ClawHub, GitHub, or other sources. It guides source reputation checks, code review, permission review, risk classification, and a structured install recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The registry display name, artifact name, and metadata slug do not fully match. <br>
Mitigation: Verify that the publisher handle, package page, artifact contents, and intended skill identity match before installing or relying on the skill. <br>
Risk: The skill provides a review checklist rather than an automatic security authority. <br>
Mitigation: Use the checklist to structure human review, and run any target-skill downloads or inspections in a temporary directory before installation. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/firebroo/security-skiil-scanner) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/firebroo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with checklists and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for optional registry or GitHub checks; supports linux, darwin, and win32 per release metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
