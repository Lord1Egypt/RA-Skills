## Description: <br>
This skill helps users migrate their local machine learning scripts to run on TensorPool GPU clusters using the interactive cluster workflow (tp ssh). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tycho-svoboda](https://clawhub.ai/user/tycho-svoboda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to adapt local machine learning training or inference scripts for TensorPool GPU clusters, including environment setup, file transfer, execution, monitoring, output retrieval, and cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead to paid TensorPool cluster creation and ongoing charges. <br>
Mitigation: Require explicit user approval before creating clusters and verify cluster destruction after the run. <br>
Risk: The skill can transfer code and environment files to remote GPU clusters, including files that may contain secrets. <br>
Mitigation: Confirm transfer scope before upload and avoid uploading raw secret files unless a secure handling method has been selected. <br>
Risk: The skill can guide package installs, SSH key creation, background jobs, persistent storage use, and code changes. <br>
Mitigation: Require explicit approval for these actions and keep code edits limited to the user's original training or inference objective. <br>


## Reference(s): <br>
- [TensorPool Docs](https://docs.tensorpool.dev) <br>
- [Cluster Quickstart](https://docs.tensorpool.dev/clusters-quickstart) <br>
- [Instance Types](https://docs.tensorpool.dev/resources/instance-types) <br>
- [CLI Reference](https://docs.tensorpool.dev/cli/overview) <br>
- [ClawHub Skill Page](https://clawhub.ai/tycho-svoboda/tensorpool) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include operational steps for paid cluster creation, remote file transfer, dependency installation, code fixes, secret handling, background jobs, storage, and cleanup.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
