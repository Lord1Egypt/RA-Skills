## Description: <br>
Agent skill quality checker. Input a skill directory or skill files; output trigger clarity, metadata issues, examples, safety boundaries, installability, portability risks, and prioritized fixes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to statically review OpenClaw skill directories for documentation quality, code and configuration issues, safety boundaries, installability, portability risks, and prioritized fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The checker reads local skill directories and writes reports or configuration files in its own directory. <br>
Mitigation: Run it only against intended skill paths and review generated files before using them for release or governance decisions. <br>
Risk: Static-analysis results are advisory and may miss issues or produce misleading findings. <br>
Mitigation: Treat reports as triage input and perform human review plus normal security scanning before deployment. <br>
Risk: Broad triggers could cause accidental activation in agent workflows. <br>
Mitigation: Invoke the skill explicitly for assessment tasks or narrow triggers when integrating it into automated workflows. <br>


## Reference(s): <br>
- [Skill Quality Checker on ClawHub](https://clawhub.ai/harrylabsj/skill-assessment) <br>
- [Publisher profile](https://clawhub.ai/user/harrylabsj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON, or plain-text static-analysis reports with prioritized findings and suggested fixes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected skill directories and can save reports under the skill's reports directory.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
