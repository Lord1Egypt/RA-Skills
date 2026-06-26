## Description: <br>
URL-encode or decode text for safe transmission in URLs and query strings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill for quick local percent-encoding and decoding of URL text while preparing links, query values, and shell-oriented workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The README advertises command flags and modes that are not present in the bundled script. <br>
Mitigation: Check the bundled script's help output before automation and use supported flags such as --encode, --decode, --component, and --plus. <br>
Risk: Using the wrong URL encoding mode can change how spaces and reserved characters are represented. <br>
Mitigation: Confirm whether percent encoding or plus-for-spaces form encoding is required before using the output in a URL or request body. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/urlencode-tool) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/dinghaibin) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plain-text encoded or decoded strings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script emits one encoded or decoded string to stdout.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
