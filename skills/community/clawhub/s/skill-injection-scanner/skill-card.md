## Description:

Scan agent skill files for hidden instructions and prompt-injection patterns (EN/RU) before a poisoned skill rewrites your agent. 19 rules, zero dependencies. Use ONLY with the user's explicit consent: tell the user which skills folder will be scanned - findings are printed to stdout locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vnbochkarev-netizen](https://clawhub.ai/user/vnbochkarev-netizen)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to scan agent skill folders for hidden instructions, prompt-injection patterns, and suspicious skill content before use or during maintenance. It is intended for local defensive review with explicit consent for the folder being scanned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports local file-read scoping and disclosure concerns.

Mitigation: Only scan folders intentionally selected by the user, disclose which folder will be read before scanning, and avoid scanning trees that may contain secrets.

Risk: The README includes npm execution guidance that the security review says should be treated cautiously.

Mitigation: Use the reviewed local scanner.py path rather than the README's npx -y command.

Risk: Scanner output can include snippets from scanned files.

Mitigation: Handle JSON output and redirected logs carefully, and delete generated logs when they are no longer needed.

Risk: The security guidance treats symlink-containing skill folders as higher risk until containment is fixed.

Mitigation: Review symlink-containing folders manually or avoid scanning them until containment behavior has been verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vnbochkarev-netizen/skills/skill-injection-scanner)
- [npm package](https://www.npmjs.com/package/@vibo-dev/skill-injection-scanner)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; scanner findings are printed as plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local stdout output may include file paths, line numbers, rule names, severity labels, and short source snippets.]

## Skill Version(s):

1.1.6 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
