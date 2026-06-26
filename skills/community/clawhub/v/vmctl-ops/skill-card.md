## Description: <br>
Use when vmctl is already installed and the agent must immediately run safe post-install checks and first lifecycle actions without guessing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bashrusakh](https://clawhub.ai/user/bashrusakh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill after vmctl is installed on a Hermes host to run health checks, smoke-test a test VM lifecycle, clean up test artifacts, recover drift, and report operator-ready status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and remove VM resources during smoke testing. <br>
Mitigation: Use it only on the intended Hermes/vmctl host and keep actions scoped to vmctl-test-* resources. <br>
Risk: Cleanup or recovery against old, ambiguous, or non-test resources could affect unintended state. <br>
Mitigation: Verify the deleted tombstone belongs to the smoke-test VM and require operator approval before recover --apply or ambiguous cleanup. <br>
Risk: Missing vmctl installation, configuration, state paths, or credentials can lead to unsafe guessing. <br>
Mitigation: Stop and ask the operator to install or configure vmctl instead of attempting bootstrap installation or credential changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bashrusakh/vmctl-ops) <br>
- [vmctl operator installation source](https://github.com/bashrusakh/vmctl) <br>
- [vmctl latest release page](https://github.com/bashrusakh/vmctl/releases/latest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise operator status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assumes vmctl, configuration, state paths, and credentials are already present; status reporting should stay limited to the requested post-install validation flow.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
