## Description: <br>
CTF-oriented ZIP cracking and recovery with the bundled ZipCracker engine for authorized analysis and recovery workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asaotomo](https://clawhub.ai/user/asaotomo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, CTF players, challenge authors, and authorized security operators use this skill to profile encrypted ZIP archives and choose an appropriate recovery path, including pseudo-encryption repair, dictionary and mask attacks, CRC32 recovery, known-plaintext workflows, template KPA, bkcrack workflows, and AES triage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be used to crack ZIP passwords. <br>
Mitigation: Use it only for CTFs, self-owned archives, or explicitly authorized recovery work; refuse requests that indicate unauthorized access to third-party data. <br>
Risk: Recovery workflows may write extracted files, recovered passwords, and logs to disk. <br>
Mitigation: Run the skill in a contained project directory with a disposable output folder and avoid storing sensitive archives or recovered material longer than necessary. <br>
Risk: Some workflows can trigger long-running dictionary or mask searches. <br>
Mitigation: Profile first, prefer strong clues over broad brute force, and require explicit user acceptance before very large mask searches. <br>
Risk: Optional dependency installation prompts can fetch external tools. <br>
Mitigation: Keep install prompts disabled unless the operator trusts the dependency sources and has approved installation in the current environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/asaotomo/zipcracker) <br>
- [Attack Playbook](references/attack-playbook.md) <br>
- [OpenClaw Workflow](references/openclaw-workflow.md) <br>
- [CTF Techniques](references/ctf-techniques.md) <br>
- [Natural Language Command Examples](references/natural-language-command-examples.md) <br>
- [Forward Test Report](references/forward-test-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include exact commands run, selected attack rationale, recovered status, blocker notes, and next-step guidance.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
