## Description: <br>
Publishes local skills to ClawHub with configurable version, display name, path, and optional changelog through a command-line or Python interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to publish a local skill directory to ClawHub, setting release metadata such as slug, display name, version, and changelog from the command line or Python API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing from an unreviewed directory can upload secrets, credentials, private notes, or unrelated files. <br>
Mitigation: Run it only from a clean package directory and inspect the files selected for upload before publishing. <br>
Risk: Credentialed publishing behavior can expose or misuse account credentials if the package is shared or run in an untrusted environment. <br>
Mitigation: Use only trusted release environments, keep credentials out of published artifacts, and rotate any exposed token before reuse. <br>
Risk: The available security evidence notes a file-upload quality issue even though the verdict is clean. <br>
Mitigation: Treat the upload issue as a quality concern to fix and verify the published files after each release. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wuhaichao87/test-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain-text guidance with command-line arguments and Python publishing results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Publishes selected local skill files and returns success or error details, including release slug, version identifier, and ClawHub URL when successful.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence and target metadata; artifact _meta.json reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
