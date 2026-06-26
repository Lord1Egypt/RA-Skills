## Description: <br>
Security-first skill vetting for AI agents before installing skills from ClawdHub, GitHub, or other sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[janeaaaa](https://clawhub.ai/user/janeaaaa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to vet external skills before installation by checking source, permissions, red flags, and risk classification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the skill's advisory vetting result as definitive. <br>
Mitigation: Review any evaluated skill yourself before installing it or granting credentials, network access, or high-impact permissions. <br>
Risk: The quick-vet examples include shell commands that fetch GitHub metadata and raw skill content. <br>
Mitigation: Run commands only against the intended repository URLs and inspect fetched content before using it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/janeaaaa/skill-checker-jane) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown vetting report with optional shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory checklist output; no executable artifact is produced by the skill itself.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
