## Description: <br>
Validate data formats including JSON, email, URL, file paths, IP addresses, and phone numbers with detailed error reporting and batch processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to validate common input formats for sanitization pipelines, CI checks, and API request validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive values supplied as command-line arguments can be captured in local shell history or process listings. <br>
Mitigation: Avoid validating real secrets or payment-card data through command-line arguments; use non-sensitive samples or an input path that does not expose values in shell history. <br>


## Reference(s): <br>
- [Validator Tool ClawHub Page](https://clawhub.ai/dinghaibin/validator-tool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Plain text or JSON validation results with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Validation results may include exit status conventions for pipeline use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
