## Description:

Automated self-diagnostics: restarts crashed Ollama, repairs broken configs, verifies workspace integrity, recovers from common failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to monitor local AI workspaces, restart local Ollama services, repair JSON configuration files, restore required workspace files from backups, and run scheduled maintenance routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic repair can overwrite local files, alter workspace state, restart services, kill processes, and run local commands.

Mitigation: Use only in a tightly scoped workspace with trusted configuration, maintain independent backups, and review automatic repair settings before enabling periodic runs.

Risk: Broad repair, process, network, and scheduling capabilities can cause service disruption if exposed to untrusted callers or unsafe custom routines.

Mitigation: Do not expose SelfRepair or RoutineManager objects to untrusted callers; restrict custom checks and routine actions to reviewed, trusted code.

Risk: Local health checks and logs may reflect workspace state and operational details.

Mitigation: Keep logs local, review log retention settings, and avoid storing sensitive data in paths or routine results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/theshadowrose/skills/self-repair-system)
- [Publisher profile](https://clawhub.ai/user/theshadowrose)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Code, Configuration, Shell commands, JSON, Guidance]

**Output Format:** [JavaScript modules with JSON health reports, repair logs, and configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local workspace paths, backup paths, required files and directories, Ollama host and port settings, custom checks, and scheduled routines.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
