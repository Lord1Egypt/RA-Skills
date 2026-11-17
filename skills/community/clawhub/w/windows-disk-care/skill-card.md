## Description:

Helps Windows users trace disk growth and, within locally authorized scopes, review cleanup candidates for old Electron packages and Cargo build caches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubai00](https://clawhub.ai/user/liubai00)

### License/Terms of Use:

MIT-0

## Use Case:

Windows developers and administrators use the skill to measure local disk growth, identify likely sources, and review cleanup candidates for regenerable development outputs under an explicitly authorized local policy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Two referenced PowerShell scripts were only partly inspected, leaving the security evidence incomplete.

Mitigation: Wait for a complete scan or review those scripts before running them.

Risk: Applying cleanup removes files selected as eligible in the preview.

Mitigation: Use a locally authorized policy, review every eligible path in the current preview, and apply only after confirming the scope.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/liubai00/skills/windows-disk-care)
- [Publisher profile](https://clawhub.ai/user/liubai00)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, PowerShell commands, JSON, Configuration guidance]

**Output Format:** [Text guidance and local JSON measurement, preview, and cleanup reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows only; requires PowerShell 7.2 or later. Cleanup is limited to locally authorized scopes and a reviewed preview.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
