## Description: <br>
Match and extract text patterns using regular expressions for data validation, text parsing, and pattern-based extraction tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to test regular expressions, extract matching text, and prepare simple pattern-based replacements in local text workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex untrusted regex patterns over very large input may be slow or produce unexpected output. <br>
Mitigation: Review patterns before use, test on representative samples, and avoid running untrusted patterns against very large input. <br>
Risk: The usage examples describe file arguments, but the script evidence shows inline text or stdin behavior. <br>
Mitigation: Confirm invocation behavior in the target environment before relying on file-path examples. <br>


## Reference(s): <br>
- [Regex Tool release page](https://clawhub.ai/dinghaibin/regex-tool) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local regex match, extraction, and replacement guidance; no external services are indicated by the evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
