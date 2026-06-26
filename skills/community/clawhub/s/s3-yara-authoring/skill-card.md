## Description: <br>
Guides agents in writing, reviewing, optimizing, and testing YARA-X malware detection rules for threat hunting with attention to naming, string selection, performance, and false-positive reduction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solomonneas](https://clawhub.ai/user/solomonneas) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security engineers, malware analysts, and threat hunters use this skill to draft and review YARA-X detection rules, convert indicators into signatures, and reduce false positives before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support security work on systems or samples outside the user's authorization. <br>
Mitigation: Use it only for systems, malware samples, and environments the user is authorized to review. <br>
Risk: Detection rules may cause false positives or miss targeted malware if deployed without validation. <br>
Mitigation: Validate syntax and behavior with YARA-X tooling, representative samples, and clean goodware sets before operational use. <br>
Risk: Prompts or outputs may include sensitive architecture, customer, credential, or sample details. <br>
Mitigation: Avoid sharing sensitive details unless the workspace and generated outputs are access-controlled. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/solomonneas/s3-yara-authoring) <br>
- [Trail of Bits YARA authoring methodology](https://github.com/trailofbits/skills/tree/main/plugins/yara-authoring) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with YARA-X code blocks and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces rule templates, review guidance, testing commands, and false-positive reduction recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
