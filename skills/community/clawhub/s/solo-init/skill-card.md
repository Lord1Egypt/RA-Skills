## Description: <br>
One-time founder onboarding that generates personalized Solo Factory configuration, including a founder manifest, STREAM calibration, development principles, and selected stack templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and solo founders use this skill for first-time Solo Factory onboarding. It asks setup questions, writes reusable org defaults, and creates local project profile files that other Solo Factory skills can read. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or update local Solo Factory configuration files. <br>
Mitigation: Run it only for a project you intend to configure, confirm the project path, and review ~/.solo-factory/defaults.yaml and .solo/ files after generation. <br>
Risk: Onboarding answers may be written into local Markdown or YAML files. <br>
Mitigation: Do not provide secrets, credentials, or sensitive private data in the setup answers. <br>
Risk: The optional Solograph check may execute an external package through uvx. <br>
Mitigation: Skip the optional Solograph/uvx check if external package execution is not desired. <br>


## Reference(s): <br>
- [Generation Rules](references/generation-rules.md) <br>
- [Question Specifications](references/questions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, shell commands, guidance] <br>
**Output Format:** [Markdown guidance plus generated YAML and Markdown configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes ~/.solo-factory/defaults.yaml and .solo/ project files based on user answers.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
