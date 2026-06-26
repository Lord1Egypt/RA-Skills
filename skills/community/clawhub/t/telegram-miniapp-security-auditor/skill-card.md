## Description: <br>
Audit Telegram Mini App projects for launch safety before connecting bot tokens or public channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to statically audit Telegram Mini App frontends, backends, BotFather launch runbooks, and related ClawHub or Codex skill packages before connecting production bot tokens or public channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated audit reports may include snippets of secrets or token-like values found in the scanned project. <br>
Mitigation: Run the auditor only against the intended project or subdirectory, write reports to a controlled output directory, limit report sharing, and rotate any real credentials found. <br>
Risk: Static audit output can miss runtime behavior or require human interpretation before launch. <br>
Mitigation: Inspect every BLOCK and REVIEW file reference, complete the Mini App security checklist, and require local or browser QA evidence before BotFather or public channel changes. <br>
Risk: The skill suggests an optional TrustClaw scan command for packaged ClawHub or Codex skills. <br>
Mitigation: Review that command and its target path separately before running it. <br>


## Reference(s): <br>
- [Telegram Mini App Security Checklist](artifact/references/tma-security-checklist.md) <br>
- [Source Homepage](https://github.com/zack-dev-cm/telegram-miniapp-security-auditor) <br>
- [ClawHub Release Page](https://clawhub.ai/zack-dev-cm/telegram-miniapp-security-auditor) <br>
- [Publisher Profile](https://clawhub.ai/user/zack-dev-cm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional shell commands, plus generated JSON and Markdown audit report files when the bundled auditor is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Audit responses lead with PASS, REVIEW, or BLOCK, followed by findings, launch recommendation, produced artifacts, and audit limitations.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
