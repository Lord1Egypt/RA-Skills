## Description: <br>
Skill Gatekeeper audits OpenClaw skills with local pattern checks, optional VirusTotal hash lookups, and quarantine handling before allowing use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanew197894fun-cmd](https://clawhub.ai/user/lanew197894fun-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill administrators use this skill to review, install, and quarantine OpenClaw skills with local checks and optional VirusTotal file-hash reputation. It is best treated as a supplemental security review workflow rather than a complete isolation boundary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install a target skill before the audit completes, so the review boundary is not fully pre-installation. <br>
Mitigation: Use only trusted slugs and perform an independent review before running unknown skills; do not treat a passing result as sole approval. <br>
Risk: Quarantine behavior can remove live installed skill directories. <br>
Mitigation: Run audits against disposable or backed-up skill directories when testing untrusted skills, especially during bulk audit. <br>
Risk: The install flow builds a shell command from the provided slug. <br>
Mitigation: Use server-resolved or otherwise trusted slugs only, and avoid unreviewed user-supplied values. <br>
Risk: VirusTotal checks use a locally stored API key and file-hash lookups. <br>
Mitigation: Avoid sensitive or private skills unless hash reputation lookups are acceptable, and protect the configured API key. <br>
Risk: The documented sandbox behavior copies files for scanning but should not be treated as real process isolation. <br>
Mitigation: Run reviews for untrusted skills in an isolated operating-system account, container, or disposable environment. <br>


## Reference(s): <br>
- [Skill Gatekeeper on ClawHub](https://clawhub.ai/lanew197894fun-cmd/skill-gatekeeper) <br>
- [Publisher profile: lanew197894fun-cmd](https://clawhub.ai/user/lanew197894fun-cmd) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bun; may use a locally configured VirusTotal API key for file-hash lookups.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
