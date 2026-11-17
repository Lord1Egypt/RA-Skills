## Description:

CTF-oriented ZIP cracking and recovery with the bundled ZipCracker engine for authorized archive analysis, pseudo-encryption repair, dictionary and mask attacks, CRC32 recovery, known-plaintext workflows, template KPA, WinZip AES triage, and large-dictionary handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[asaotomo](https://clawhub.ai/user/asaotomo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, CTF players, challenge authors, and authorized recovery operators use this skill to profile encrypted ZIP archives, choose an evidence-based recovery tactic, run the bundled wrapper, and report the command, rationale, and result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used for ZIP password recovery and may be inappropriate for unauthorized access attempts.

Mitigation: Use only for CTFs, self-owned archives, or explicitly authorized recovery, and refuse requests that suggest unauthorized third-party access.

Risk: Extraction and optional dependency-install paths create high-impact filesystem and supply-chain risks.

Mitigation: Review before installing, prefer a disposable workspace or container, preinstall pinned dependencies where possible, avoid --allow-install-prompts unless mutable downloads are accepted, and avoid pointing --out at important existing directories until the flagged issues are fixed.

## Reference(s):

- [ZipCracker Skill Page](https://clawhub.ai/asaotomo/skills/zipcracker)
- [Attack Playbook](references/attack-playbook.md)
- [CTF Techniques](references/ctf-techniques.md)
- [OpenClaw Workflow](references/openclaw-workflow.md)
- [Natural Language Command Examples](references/natural-language-command-examples.md)
- [Forward Test Report](references/forward-test-report.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Markdown, Configuration]

**Output Format:** [Markdown with inline bash commands and concise run summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected wrapper flags, archive profile observations, recovered password or extraction status when authorized, and next-step guidance when recovery is blocked.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
