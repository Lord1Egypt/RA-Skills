# Risk Warnings for Task Verification

Security and compliance guidance when reviewing OpenAnt submissions.

## Do NOT Execute Untrusted Code or Files

- **Never run executables** (.exe, .sh, .bat, .ps1, binaries) from submissions without explicit user approval and sandboxing.
- **Never execute scripts** (Python, Node, etc.) from unknown sources — they may exfiltrate data, install malware, or modify your system.
- **Prefer read-only operations** — Extract text, parse JSON, view in browser. Do not `eval`, `exec`, or `require` submission content.
- If you must run code to verify (e.g., unit tests), use an isolated environment (sandbox, VM, container) and get user confirmation.

## Privacy and Data Protection

- **Do not extract or store PII** from submissions beyond what is needed for the review (e.g., task-relevant content only).
- **Do not forward submission content** to third parties without user consent.
- **Proof URLs** — Opening a GitHub PR or deployed site is generally safe. Avoid URLs that prompt for credentials or download unknown files.
- **Sensitive data** — If a submission contains API keys, passwords, or personal data, flag it and do not log or reuse it.

## Compliance with Task Requirements

- **Scope** — Only approve work that meets the task description. Reject off-topic or incomplete deliverables.
- **Integrity** — Reject plagiarized or AI-generated content when the task explicitly forbids it.
- **Licensing** — If the task requires original work or specific licenses, verify compliance before approving.

## Red Flags

| Red flag | Action |
|----------|--------|
| Executable or script in submission | Do not run. Inspect metadata only or ask user. |
| URL redirects to download | Do not download. Report to user. |
| Submission contains credentials | Reject; advise worker to rotate keys. |
| Content is off-topic or spam | Reject with clear feedback. |
| Proof URL requires login | Reject — reviewer must be able to verify without auth. |

## Summary

- **Read, don't run** — Prefer inspection over execution.
- **No PII leakage** — Handle submission data with care.
- **Match task scope** — Approve only compliant work.
- **When in doubt** — Ask the user before taking irreversible actions.
