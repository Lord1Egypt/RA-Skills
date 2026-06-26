## Description: <br>
SkillWiki helps agents analyze and review ClawHub skills by downloading a ClawHub package, extracting structured metadata, and producing a Markdown skill analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skinapi2025](https://clawhub.ai/user/skinapi2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and skill reviewers use SkillWiki to inspect ClawHub skills before installation, compare skill behavior, and summarize security-relevant package metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and extracts ClawHub skill packages from a configured endpoint before analysis. <br>
Mitigation: Run it only for ClawHub packages you intend to inspect, keep the endpoint configuration trusted, and review downloaded package results before acting on recommendations. <br>
Risk: The workflow intentionally reviews the downloaded ClawHub package and may not reflect unpublished or locally modified skill files. <br>
Mitigation: Inspect local or unpublished files separately when assessing local changes. <br>
Risk: The security evidence notes hardening gaps despite a clean scanner verdict. <br>
Mitigation: Treat reports as decision support, review security findings manually, and scan skills before deployment. <br>


## Reference(s): <br>
- [ClawHub SkillWiki release page](https://clawhub.ai/skinapi2025/skillwiki) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/skinapi2025) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown analysis with inline shell commands and optional JSON extraction output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports follow the configured language preference and may include security, dependency, quality, and usage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
