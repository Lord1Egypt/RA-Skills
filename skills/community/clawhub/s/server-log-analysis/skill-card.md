## Description:

Connects to remote servers over SSH, reads config.yaml for service and log locations, downloads targeted log segments into a local temp directory, and analyzes them to diagnose service issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgvgfgvh](https://clawhub.ai/user/hgvgfgvh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and site reliability engineers use this skill to diagnose remote service failures by matching an incident to configured services, collecting the smallest useful log segments, and producing an evidence-based diagnosis with follow-up checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires SSH-based access to remote servers for log diagnosis.

Mitigation: Use least-privilege log-reading accounts, key-based or environment-provided credentials, and confirm target hosts before connecting.

Risk: Downloaded logs may contain sensitive operational or user data and may be preserved locally.

Mitigation: Download only minimal relevant segments, avoid unrelated sensitive files, and protect or clean temp/server-log-analysis according to local policy.

Risk: The sample configuration includes root and password placeholders that could encourage unsafe credential storage.

Mitigation: Replace sample values with a non-root log-reading account and external secret management; do not store real secrets in config.yaml.

## Reference(s):

- [Reference Guide](artifact/reference.md)
- [ClawHub Skill Page](https://clawhub.ai/hgvgfgvh/skills/server-log-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic summary with evidence, confidence, and next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include references to downloaded local log snippets; downloads are kept under temp/server-log-analysis unless configured otherwise.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
