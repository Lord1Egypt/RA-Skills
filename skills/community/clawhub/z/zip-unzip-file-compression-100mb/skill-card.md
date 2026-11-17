## Description:

Compresses and decompresses 10MB to 100MB ZIP and GZIP archives through AgentPMT, returning cloud-stored outputs with signed download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to package, unpack, and share large datasets, media bundles, logs, exports, or deployment archives through AgentPMT-hosted archive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Archive contents and extracted files are sent to AgentPMT cloud storage and returned through signed URLs.

Mitigation: Use the skill only for data approved for that storage model, and avoid confidential, regulated, or customer-sensitive archives unless organizational policy allows it.

Risk: The skill relies on mutable remote instructions and setup commands that may change after installation.

Mitigation: Review live schemas and instructions before production use, prefer pinned or reviewed setup packages, and require explicit approval before expanding data sent, destinations, credential requests, or security rules.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agentpmt/skills/zip-unzip-file-compression-100mb)
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/zip-unzip-file-compression-100mb)
- [Generated action schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [API Calls, Files, Guidance]

**Output Format:** [JSON responses with file IDs, size metadata, and signed download URLs for compressed or extracted files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports ZIP and GZIP archives from 10MB to 100MB; ZIP compression supports up to 500 files; signed URLs expire after 7 days.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
