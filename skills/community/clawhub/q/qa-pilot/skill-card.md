## Description:

QA Pilot gives AI agents a framework-agnostic methodology for testing websites and applications, fixing discovered issues, and reporting completion only after verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helal-muneer](https://clawhub.ai/user/helal-muneer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agent builders, and AI-assisted app creators use QA Pilot to make an agent test built or modified apps against the original request, exercise user workflows, fix defects, and provide an honest QA report before declaring work complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives agents broad permission to perform active QA and automatic fix attempts.

Mitigation: Run it only on local or explicitly approved test environments, and keep the scope limited to the app or workflow being evaluated.

Risk: Testing against production, admin consoles, payments, messaging, or third-party systems can cause unintended actions or data exposure.

Mitigation: Avoid those targets unless explicitly approved; use test accounts, disposable data, and cleanup steps after testing.

Risk: The install guidance includes an unpinned npx command.

Mitigation: Prefer a pinned or trusted install path before enabling the skill in an agent environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/helal-muneer/skills/qa-pilot)
- [Publisher Profile](https://clawhub.ai/user/helal-muneer)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [SECURITY.md](artifact/SECURITY.md)
- [CHANGELOG.md](artifact/CHANGELOG.md)
- [Demo README](artifact/demo/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown methodology with checklists, QA report templates, YAML configuration examples, and shell command snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single-stream agent guidance; use should be scoped to approved local or test environments because it can prompt active browser testing, dev-server use, and fix attempts.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact skill metadata, and CHANGELOG dated 2026-04-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
