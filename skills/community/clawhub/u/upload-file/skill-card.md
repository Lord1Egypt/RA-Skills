## Description: <br>
Automates user-directed browser file uploads through agent-browser CLI with a step-by-step execution protocol, fallback selectors, path normalization, and upload verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[m1ss-cell](https://clawhub.ai/user/m1ss-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need to upload a specific local file to a web page through browser automation and verify that the upload succeeded. Users should confirm the destination site and resolved file path before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload local files to a website selected by the agent or user. <br>
Mitigation: Confirm the exact destination website and resolved local file path before execution. <br>
Risk: Sensitive or unintended files could be uploaded if the file path is wrong or expands unexpectedly. <br>
Mitigation: Avoid uploading secrets, credentials, identity documents, medical or financial records, or internal files unless that is explicitly intended. <br>
Risk: The documentation references scripts/upload_file.py while the artifact contains scripts/upload.py. <br>
Mitigation: Use scripts/upload.py unless a future package version adds or renames the documented script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/m1ss-cell/upload-file) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands and a Python helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces browser upload steps and command invocations for agent-browser; no structured API response is defined.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
