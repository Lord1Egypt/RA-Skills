## Description: <br>
Validate emails, URLs, phones, dates, and custom patterns for input checks and rule enforcement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to validate common input formats, check file syntax, and enforce simple data quality rules during development or operational workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: URL and domain checks can make outbound HTTP requests or DNS lookups for supplied inputs. <br>
Mitigation: Run network-checking commands only when outbound requests are acceptable for the target environment and input. <br>
Risk: The JSON and YAML file validators have unsafe filename handling that could execute unintended code for untrusted or oddly named files. <br>
Mitigation: Avoid using the JSON or YAML validators on untrusted filenames until filename handling is fixed. <br>


## Reference(s): <br>
- [Validator on ClawHub](https://clawhub.ai/xueyetianya/validator) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation commands may return non-zero exit codes for invalid inputs.] <br>

## Skill Version(s): <br>
3.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
