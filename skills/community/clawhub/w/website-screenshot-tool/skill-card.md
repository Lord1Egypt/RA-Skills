## Description: <br>
Automated website screenshot tool with responsive capture, batch processing, visual comparison, and scheduled monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to capture webpage screenshots, run responsive viewport checks, compare webpage versions, and maintain screenshot history for monitoring workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated browser visits may reach private or internal sites if the runtime has network access. <br>
Mitigation: Run the skill only in environments where visiting the provided URLs is acceptable, and isolate browser automation from sensitive networks when possible. <br>
Risk: Unpinned browser automation dependencies can change behavior across installs. <br>
Mitigation: Pin dependencies with a lockfile before serious production or CI use. <br>
Risk: Screenshot and history outputs may contain sensitive webpage content. <br>
Mitigation: Use a dedicated output directory with appropriate access controls and retention practices. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/website-screenshot-tool) <br>
- [Publisher Profile](https://clawhub.ai/user/kaiyuelv) <br>
- [README](README.md) <br>
- [Dependency Manifest](requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell snippets; generated artifacts are PNG screenshots and JSON history files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write screenshot image files and JSON history records to a configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
