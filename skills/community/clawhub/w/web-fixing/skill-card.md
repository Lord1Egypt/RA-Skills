## Description:

Helps agents systematically diagnose and fix web and frontend issues, including UI defects, responsive layout problems, CSS issues, JavaScript errors, broken interactions, and post-generation page checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aqbjqtd](https://clawhub.ai/user/aqbjqtd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents through root-cause analysis, minimal fixes, and verification for web UI, responsiveness, JavaScript, CSS, and performance issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional unpinned npm and Playwright setup commands can change installed dependencies or system packages.

Mitigation: Pin package versions, prefer an existing lockfile or npm ci, and avoid --with-deps outside a disposable container or explicitly approved development machine.

Risk: The skill is intended for agents with normal project read and edit authority for front-end fixes.

Mitigation: Install only where that project access is acceptable, review proposed edits, and scan the skill before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aqbjqtd/skills/web-fixing)
- [Detailed workflows](artifact/references/workflows.md)
- [Repair checklist](artifact/references/checklist.md)
- [Repair examples](artifact/references/examples.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verification checklists and browser or device testing steps.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
